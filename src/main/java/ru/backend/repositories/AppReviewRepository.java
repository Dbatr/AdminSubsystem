package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.AppReview;

@Repository
public interface AppReviewRepository extends JpaRepository<AppReview, Long> {
}
