from dataclasses import dataclass

from app.domain.entity.assignment_entity import AssignmentEntity, AssignmentStatus
from app.domain.interfaces.assignment_repository import AssignmentRepository
from app.domain.exceptions.not_found import AssignmentNotFoundException
from app.domain.exceptions.business_rules import InvalidAssignmentStatusTransitionException


@dataclass
class UpdateAssignmentStatusCommand:
    assignment_id: int
    status: AssignmentStatus


class UpdateAssignmentStatusUseCase:
    def __init__(self, assignment_repository: AssignmentRepository) -> None:
        self._assignment_repository = assignment_repository

    async def execute(self, command: UpdateAssignmentStatusCommand) -> AssignmentEntity:
        assignment = await self._assignment_repository.find_by_id(command.assignment_id)
        if not assignment:
            raise AssignmentNotFoundException(command.assignment_id)

        if command.status == AssignmentStatus.COMPLETED:
            assignment.complete()
        elif command.status == AssignmentStatus.CANCELLED:
            assignment.cancel()
        else:
            raise InvalidAssignmentStatusTransitionException(assignment.status, command.status)

        return await self._assignment_repository.update(assignment)
