WITH stage_lengths as (
	SELECT
		sk_subject,
		max(substr(stage_id, 2)::int)*20 as max_progress_point
	FROM dim_stage
	GROUP BY 1	
),

calculated_ages as (
	SELECT
		fact_id
		, date_id
		, year
		, month
		, date_of_birth
		, date_part('year', age(concat(year, '-', month, '-', 20)::date, date_of_birth))::int as age_at_report
	FROM fact_student_monthly_performance f
	JOIN dim_student ds on ds.sk_student = f.sk_student
	JOIN dim_date dd on dd.sk_date = f.sk_date
)

SELECT
	f.fact_id
	, dd.date_id
	, dd.year
	, dd.month
	, student_id
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
	, subject
	, stage_id
	, stage_name
	, grade_name
	, type_description
	, advanced_flag
	, scholarship_flag
	, current_lesson
	, total_sheets
	
	-- Average number of sheets for the last 3 months
	, round(avg(total_sheets) over (partition by student_id
									order by dd.year, dd.month
							  	    rows between 2 preceding and current row)) as avg_total_sheets_3

	-- Is stalled
	, case 
		when (current_lesson - lag(current_lesson) over (partition by student_id order by dd.year, dd.month)) <= 0 then 1 
		else 0
	  end as stalled

	-- Global block number							  
	, (((substr(stage_id, 2)::int-1)*200 + current_lesson)/10) as progress_point
	
	-- Course completion %
    , round((((substr(stage_id, 2)::int-1)*200 + current_lesson)/10 ) / max_progress_point::decimal * 100, 2) as progress_pct

	-- Target
	, status_name
	
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

WHERE full_name = 'REBEKAH CÂNDIDO TESCH' and subject = 'math'

ORDER BY fact_id;