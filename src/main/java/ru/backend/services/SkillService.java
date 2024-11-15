package ru.backend.services;

import java.util.List;
import java.util.Optional;
import ru.backend.dtos.SkillDTO;
import ru.backend.models.crm.Skill;

public interface SkillService {

    List<Skill> getAllSkills();

    // Получение навыка по ID
    Optional<Skill> getSkillById(Integer id);

    // Добавление нового навыка
    Skill addSkill(SkillDTO skillDTO);

    // Удаление навыка по ID
    void deleteSkill(Integer id);
}
