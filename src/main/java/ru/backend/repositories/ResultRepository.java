package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.canban.Result;

@Repository
public interface ResultRepository extends JpaRepository<Result, Long> {
}
