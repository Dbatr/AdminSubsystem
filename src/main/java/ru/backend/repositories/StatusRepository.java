package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.canban.Status;

@Repository
public interface StatusRepository extends JpaRepository<Status, Long> {
}
