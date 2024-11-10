package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.backend.models.Skill;

public interface SkillRepository extends JpaRepository<Skill, Integer> {
}
