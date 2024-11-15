package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.backend.models.crm.Direction;

public interface DirectionRepository extends JpaRepository<Direction, Integer> {
}
