package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.canban.Task;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
}
