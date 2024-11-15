package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import ru.backend.models.crm.Skill;

import java.util.Set;

public interface SkillRepository extends JpaRepository<Skill, Integer> {
    Set<Skill> findAllById(Integer id);
}
