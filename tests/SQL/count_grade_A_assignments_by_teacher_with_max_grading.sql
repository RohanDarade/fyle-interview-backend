-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_grades AS (
    SELECT 
        teacher_id,
        COUNT(*) AS total_assignments,
        SUM(CASE WHEN grade = 'A' THEN 1 ELSE 0 END) AS grade_a_count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
),
max_grading_teacher AS (
    SELECT 
        teacher_id
    FROM teacher_grades
    ORDER BY total_assignments DESC
    LIMIT 1
)
SELECT 
    tg.grade_a_count
FROM teacher_grades tg
JOIN max_grading_teacher mgt ON tg.teacher_id = mgt.teacher_id;
