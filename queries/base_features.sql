WITH 
stage_lengths as (
	SELECT
		sk_subject,
		max(substr(stage_id, 2)::int)*20 as max_progress_point
	FROM dim_stage
	GROUP BY 1	
)

, calculated_ages as (
	SELECT
		fact_id
		, year
		, month
		, date_of_birth
		, date_part('year', age(concat(year, '-', month, '-', 20)::date, date_of_birth))::int as age_at_report
	FROM fact_student_monthly_performance f
	JOIN dim_student ds on ds.sk_student = f.sk_student
	JOIN dim_date dd on dd.sk_date = f.sk_date
)

, lesson_differences as (
	SELECT
		f.fact_id
		, year
		, month
		, student_id
		, subject
		, 200* trim(leading 'mpij' from stage_id)::int - 
	      200* (lag(trim(leading 'mpij' from stage_id)::int, 1, 0)
	            over (partition by student_id, subject order by year, month)) + 
	      current_lesson - 
	      (lag(current_lesson, 1, 0) over (partition by student_id, subject order by year, month)) as lesson_delta
	FROM fact_student_monthly_performance f
	JOIN dim_date dd on dd.sk_date = f.sk_date
	JOIN dim_student ds on ds.sk_student = f.sk_student
	JOIN dim_subject dsub on dsub.sk_subject = f.sk_subject
	JOIN dim_stage dstg on dstg.sk_stage = f.sk_stage	
)

, sheets_statistics as (
	SELECT
		f.fact_id
		, year
		, month
		, student_id
		, subject
		, avg(total_sheets) over (partition by ds.student_id, dsub.subject
									order by dd.year, dd.month
							  	    rows between 3 preceding and 1 preceding) as avg_sheets_3
		, stddev(total_sheets) over (partition by ds.student_id, dsub.subject
									order by dd.year, dd.month
							  	    rows between 3 preceding and 1 preceding) as stddev_sheets_3
	FROM fact_student_monthly_performance f
	JOIN dim_date dd on dd.sk_date = f.sk_date
	JOIN dim_student ds on ds.sk_student = f.sk_student
	JOIN dim_subject dsub on dsub.sk_subject = f.sk_subject
)

SELECT
	f.fact_id
	, dd.date_id
	, dd.year
	, dd.month
	, ds.student_id
	, full_name
	, ds.date_of_birth
	, age_at_report
	, case 
		when age_at_report < 7 then 'early childhood'
		when age_at_report between 7 and 14 then 'school age'
		when age_at_report between 15 and 18 then 'teenager'
		when age_at_report between 18 and 25 then 'young adult'
		when age_at_report > 25 then 'adult'
	  end as life_stage		
	, gender
	, type_description
	, advanced_flag
	, scholarship_flag
	, dsub.subject
	, trim(leading 'mpij' from stage_id)::int as stage_number
	, stage_name
	, grade_name
	
-- Measurements

	, current_lesson
	, total_sheets
	
	-- Global block number							  
	, (((substr(stage_id, 2)::int-1)*200 + current_lesson)/10) as progress_point
	
	-- Course completion %
    , round((((substr(stage_id, 2)::int-1)*200 + current_lesson)/10 ) / max_progress_point::decimal * 100, 2) as progress_pct

	-- How many stages until advanced 
	, case 
		when dsub.subject = 'japanese' then null
	    else grade_id::int - stage_grade
	  end as stages_to_adv

	-- Real progress comparing with the previous month (binary)
	, case 
		when lesson_delta <= 0 then 1 
		else 0
	  end as is_stalled

	-- Average number of sheets for the last 3 months
	, round(avg_sheets_3)

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
			and advanced_flag = 0
			and 
				((dsub.subject = 'portuguese' and age_at_report < 9 and stage_grade <= 1)
				  or 
				 (dsub.subject in ('math', 'english', 'japanese') and stage_grade <=9))
			then 1
		else 0
	  end as bad_churn
FROM fact_student_monthly_performance f

JOIN dim_date dd on dd.sk_date = f.sk_date
JOIN dim_student ds on ds.sk_student = f.sk_student
JOIN dim_subject dsub on dsub.sk_subject = f.sk_subject
JOIN dim_stage dstg on dstg.sk_stage = f.sk_stage
JOIN dim_grade dg on dg.sk_grade = f.sk_grade
JOIN dim_studytype dstp on dstp.sk_studytype = f.sk_studytype
JOIN dim_advanced da on da.sk_advanced = f.sk_advanced
JOIN dim_scholarship dsc on dsc.sk_scholarship = f.sk_scholarship
JOIN dim_status dstat on dstat.sk_status = f.sk_status

JOIN stage_lengths sl on f.sk_subject = sl.sk_subject
JOIN calculated_ages ca on f.fact_id = ca.fact_id
JOIN lesson_differences ld on f.fact_id = ld.fact_id
JOIN sheets_statistics ss on f.fact_id = ss.fact_id

ORDER BY fact_id;