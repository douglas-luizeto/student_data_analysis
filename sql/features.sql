WITH 
student_metrics as (
	SELECT
		f.fact_id
		, date_part('year', age(concat(year, '-', month, '-', 01)::date, date_of_birth))::int as age_at_report
		, avg(total_sheets) over (partition by ds.student_id, dsub.subject
								  order by dd.year, dd.month
							  	  rows between 3 preceding and 1 preceding) as avg_sheets_3
		, stddev(total_sheets) over (partition by ds.student_id, dsub.subject
									 order by dd.year, dd.month
							  	     rows between 3 preceding and 1 preceding) as stddev_sheets_3
	    , lead(concat(year, '-', month, '-', 01)::date, 3) over (partition by ds.student_id, dsub.subject
								                                 order by dd.year, dd.month) as date_3m_future
																 
	    , lead(concat(year, '-', month, '-', 01)::date, 6) over (partition by ds.student_id, dsub.subject
								                                 order by dd.year, dd.month) as date_6m_future
	    
		, lead(concat(year, '-', month, '-', 01)::date, 9) over (partition by ds.student_id, dsub.subject
								                                 order by dd.year, dd.month) as date_9m_future
		
		, lead(concat(year, '-', month, '-', 01)::date, 12) over (partition by ds.student_id, dsub.subject
								                                  order by dd.year, dd.month) as date_12m_future

		, lead(concat(year, '-', month, '-', 01)::date, 24) over (partition by ds.student_id, dsub.subject
								                                  order by dd.year, dd.month) as date_24m_future
		, count(f.fact_id) over (partition by ds.student_id, dsub.subject
			      			     order by dd.year, dd.month
						         rows between unbounded preceding and current row) as months_at_report
														 
	FROM fact_student_monthly_performance f
	JOIN dim_date dd on dd.sk_date = f.sk_date
	JOIN dim_student ds on ds.sk_student = f.sk_student
	JOIN dim_subject dsub on dsub.sk_subject = f.sk_subject
)
SELECT
	f.fact_id
	-- , full_name
	, dd.date_id
	, dd.year
	, dd.month
	, ds.student_id
	, age_at_report
	, case 
		when age_at_report < 7 then 'early childhood'
		when age_at_report between 7 and 14 then 'school age'
		when age_at_report between 15 and 18 then 'teenager'
		when age_at_report between 18 and 25 then 'young adult'
		when age_at_report > 25 then 'adult'
	  end as life_stage		
	, first_value(dd.date_id) over (partition by f.sk_student, f.sk_subject order by dd.date_id) as enroll_date
	, advanced_flag
	, dsub.subject
 	, stage_name
	, grade_name
	-- Hard-coded number of instructors available at report date
	, case
		when dd.date_id < '202208' then 3
		when dd.date_id between '202208' and '202303' then  4
		when dd.date_id between '202304' and '202401' then  3
		when dd.date_id > '202401' then  2
	  end as number_of_instructors
	
-- Measurements
	, total_sheets

	-- Months since enrollment
	-- Whenever a student is marked as absent in the report, they were not enrolled that month.
	-- Hence, months_enrolled shows the last value before churn. 
	, case when status_name in ('absent', 'absent_graduate', 'absent_transfer') 
		        then months_at_report - 1 else months_at_report
	  end as months_enrolled

	-- Survives 3 months (IC3)
	, case when date_3m_future is not null
				and (lead(status_name, 3) over (partition by ds.student_id, dsub.subject 
												order by dd.year, dd.month)) = 'current'
	            and date_3m_future = concat(year, '-', month, '-', 01)::date + interval '3 month'
		   then 1 else 0 
	  end as ic3_flag
	
	-- Survives 6 months (IC6)
	, case when date_6m_future is not null
				and (lead(status_name, 6) over (partition by ds.student_id, dsub.subject 
												order by dd.year, dd.month)) = 'current'
	            and date_6m_future = concat(year, '-', month, '-', 01)::date + interval '6 month'
		   then 1 else 0 
	  end as ic6_flag
	
	-- Survives 9 months (IC9)
	, case when date_9m_future is not null
				and (lead(status_name, 6) over (partition by ds.student_id, dsub.subject 
												order by dd.year, dd.month)) = 'current'
	            and date_9m_future = concat(year, '-', month, '-', 01)::date + interval '9 month'
		   then 1 else 0 
	  end as ic9_flag
	  
	-- Survives 12 months (IC12)
	, case when date_12m_future is not null
			    and (lead(status_name, 6) over (partition by ds.student_id, dsub.subject 
												order by dd.year, dd.month)) = 'current'
	            and date_12m_future = concat(year, '-', month, '-', 01)::date + interval '12 month'
		   then 1 else 0 
	  end as ic12_flag
	  
	-- Survives 24 months (IC24)
	, case when date_24m_future is not null
	            and (lead(status_name, 6) over (partition by ds.student_id, dsub.subject 
												order by dd.year, dd.month)) = 'current'
	            and date_24m_future = concat(year, '-', month, '-', 01)::date + interval '24 month'
		   then 1 else 0 
	  end as ic24_flag
		   
	-- How many stages until advanced 
	, case 
		when dsub.subject = 'japanese' then null
	    else grade_id::int - stage_grade
	  end as stages_to_adv

	-- Months at same stage
	, count(f.sk_stage) over (partition by f.sk_student, f.sk_subject, f.sk_stage 
						    order by dd.date_id
							rows between unbounded preceding and current row) as months_at_same_stage

	-- Coefficient of variation (stddev/average) of the number of sheets in last 3 months
	, case 
		when 
			status_name in ('new', 'new_former', 'new_transfer') then null
		when 
			avg_sheets_3 = 0 then 10
		else	
			round(stddev_sheets_3 / avg_sheets_3, 2)
	  end as cv_3
	
	-- Target
	, status_name
	, case
		when
			status_name not in ('absent', 'absent_transfer', 'absent_graduate')
			then null
		when
			status_name in ('absent', 'absent_transfer')
			-- not advanced cutoff
			and advanced_flag = 0
			and 
			    -- literacy cutoff
				((dsub.subject = 'portuguese' and age_at_report < 9 and stage_grade <= 1)
				  or
				-- middle school cutoff
				 (dsub.subject = 'portuguese' and age_at_report >= 9 and stage_grade <= 9)
				  or
				 (dsub.subject in ('math', 'english') and stage_grade <=9))
				  or
				-- intermediate level cutoff
				 (dsub.subject in ('japanese') and stage_name not in ('J', 'K', 'L'))
			then 1
		else 0
	  end as bad_churn
FROM fact_student_monthly_performance f

JOIN dim_date dd on dd.sk_date = f.sk_date
JOIN dim_student ds on ds.sk_student = f.sk_student
JOIN dim_subject dsub on dsub.sk_subject = f.sk_subject
JOIN dim_stage dstg on dstg.sk_stage = f.sk_stage
JOIN dim_grade dg on dg.sk_grade = f.sk_grade
JOIN dim_advanced da on da.sk_advanced = f.sk_advanced
JOIN dim_status dstat on dstat.sk_status = f.sk_status

JOIN student_metrics sm on f.fact_id = sm.fact_id

ORDER BY fact_id;