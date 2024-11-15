package ru.backend.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.backend.dtos.SkillDTO;
import ru.backend.models.crm.Skill;
import ru.backend.repositories.SkillRepository;

import java.util.List;
import java.util.Optional;

@Service
public class SkillService {
    private final SkillRepository skillRepository;

    @Autowired
    public SkillService(SkillRepository skillRepository) {
        this.skillRepository = skillRepository;
    }

    // Получение всех навыков
    public List<Skill> getAllSkills() {
        return skillRepository.findAll();
    }

    // Получение навыка по ID
    public Optional<Skill> getSkillById(Integer id) {
        return skillRepository.findById(id);
    }

    // Добавление нового навыка
    public Skill addSkill(SkillDTO skillDTO) {
        Skill skill = new Skill();
        skill.setName(skillDTO.getName());
        return skillRepository.save(skill);
    }

    // Удаление навыка по ID
    public void deleteSkill(Integer id) {
        skillRepository.deleteById(id);
    }
}
