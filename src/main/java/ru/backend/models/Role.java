package ru.backend.models;

import jakarta.persistence.*;
import lombok.Data;

@Entity
@Table(name = "crm_role")
@Data
public class Role {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;
    @Column(name = "name", nullable = false, length = 50)
    private String name;
}
