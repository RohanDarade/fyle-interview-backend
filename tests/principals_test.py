from core.models.assignments import AssignmentStateEnum, GradeEnum


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 5,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.C


def test_regrade_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

# New tests added to increase to coverage
def test_get_teachers(client, h_principal, teachers):
    response = client.get('/principal/teachers', headers=h_principal)
    assert response.status_code == 200

    data = response.json['data']
    assert len(data) == len(teachers)
    for teacher in data:
        assert 'id' in teacher
        assert 'user_id' in teacher
        assert 'created_at' in teacher
        assert 'updated_at' in teacher


def test_grade_assignment_invalid_payload(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={},
        headers=h_principal
    )
    assert response.status_code == 400


def test_grade_assignment_bad_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'AB'
        },
        headers=h_principal
    )
    assert response.status_code == 400


def test_grade_assignment_bad_assignment(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 100,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )
    assert response.status_code == 404

