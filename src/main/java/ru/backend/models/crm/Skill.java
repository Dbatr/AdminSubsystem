package ru.backend.models.crm;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "crm_skill")
@Data
public class Skill {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "name", nullable = false, unique = true)
    private String name;
}
