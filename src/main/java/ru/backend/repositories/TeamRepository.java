package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.Team;

@Repository
public interface TeamRepository extends JpaRepository<Team, Long> {
}
