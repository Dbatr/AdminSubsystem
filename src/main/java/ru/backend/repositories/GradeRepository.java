package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.canban.Grade;

@Repository
public interface GradeRepository extends JpaRepository<Grade, Long> {
}
