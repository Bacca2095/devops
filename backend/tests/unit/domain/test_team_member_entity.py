from app.domain.entity.team_member_entity import TeamMemberEntity, MemberStatus


class TestTeamMemberEntityStatusToggle:
    def test_active_member_is_active(self, active_member: TeamMemberEntity):
        assert active_member.is_active() is True

    def test_inactive_member_is_not_active(self, inactive_member: TeamMemberEntity):
        assert inactive_member.is_active() is False

    def test_deactivate_active_member(self, active_member: TeamMemberEntity):
        active_member.deactivate()
        assert active_member.status == MemberStatus.INACTIVE
        assert active_member.is_active() is False

    def test_activate_inactive_member(self, inactive_member: TeamMemberEntity):
        inactive_member.activate()
        assert inactive_member.status == MemberStatus.ACTIVE
        assert inactive_member.is_active() is True
