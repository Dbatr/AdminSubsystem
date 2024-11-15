package ru.backend.services.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import ru.backend.dtos.SkillDTO;
import ru.backend.models.crm.Skill;
import ru.backend.repositories.SkillRepository;
import ru.backend.services.SkillService;

import java.util.List;
import java.util.Optional;

@Service
public class SkillServiceImpl implements SkillService {
    private final SkillRepository skillRepository;

    @Autowired
    public SkillServiceImpl(SkillRepository skillRepository) {
        this.skillRepository = skillRepository;
    }

    @Override
    public List<Skill> getAllSkills() {
        return skillRepository.findAll();
    }

    @Override
    public Optional<Skill> getSkillById(Integer id) {
        return skillRepository.findById(id);
    }

    @Override
    public Skill addSkill(SkillDTO skillDTO) {
        Skill skill = new Skill();
        skill.setName(skillDTO.getName());
        return skillRepository.save(skill);
    }

    @Override
    public void deleteSkill(Integer id) {
        skillRepository.deleteById(id);
    }
}
