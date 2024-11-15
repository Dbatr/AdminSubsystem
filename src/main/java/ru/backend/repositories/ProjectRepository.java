package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.Project;

@Repository
public interface ProjectRepository extends JpaRepository<Project, Long> {
}
