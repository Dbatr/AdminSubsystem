package ru.backend.models.crm;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.util.Set;

@Entity
@Getter
@Setter
@Table(name = "crm_team")
public class Team {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @ManyToOne
    @JoinColumn(name = "direction_id", nullable = false)
    private Direction direction;

    @ManyToMany
    @JoinTable(
            name = "crm_team_students",
            joinColumns = @JoinColumn(name = "team_id"),
            inverseJoinColumns = @JoinColumn(name = "profile_id"))
    private Set<Profile> students;

    @ManyToOne
    @JoinColumn(name = "curator_id", nullable = true)
    private Profile curator;

    @Override
    public String toString() {
        return name;
    }
}
