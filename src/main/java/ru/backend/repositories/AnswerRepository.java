package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.Answer;

@Repository
public interface AnswerRepository extends JpaRepository<Answer, Long> {
}
