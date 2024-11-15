package ru.backend.controllers;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.backend.dtos.SkillDTO;
import ru.backend.models.crm.Skill;
import ru.backend.services.SkillService;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/skills")
public class SkillController {
    private final SkillService skillService;

    @Autowired
    public SkillController(SkillService skillService) {
        this.skillService = skillService;
    }

    @GetMapping
    public List<Skill> getAllSkills() {
        return skillService.getAllSkills();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Skill> getSkillById(@PathVariable Integer id) {
        Optional<Skill> skill = skillService.getSkillById(id);
        return skill.map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    @PostMapping
    public ResponseEntity<Skill> addSkill(@RequestBody SkillDTO skill) {
        if (skill.getName() == null || skill.getName().isEmpty()) {
            return ResponseEntity.badRequest().build();
        }
        Skill savedSkill = skillService.addSkill(skill);
        return ResponseEntity.ok(savedSkill);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteSkill(@PathVariable Integer id) {
        if (skillService.getSkillById(id).isPresent()) {
            skillService.deleteSkill(id);
            return ResponseEntity.noContent().build();
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
