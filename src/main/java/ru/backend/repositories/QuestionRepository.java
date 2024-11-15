package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.Question;

@Repository
public interface QuestionRepository extends JpaRepository<Question, Long> {
}
