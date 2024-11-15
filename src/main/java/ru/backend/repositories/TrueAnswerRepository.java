package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.TrueAnswer;

@Repository
public interface TrueAnswerRepository extends JpaRepository<TrueAnswer, Long> {
}
