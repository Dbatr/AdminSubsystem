package ru.backend.models.crm;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import java.time.LocalDate;
import java.util.Set;

@Entity
@Getter
@Setter
@Table(name = "crm_project")
public class Project {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(length = 10000)
    private String description;

    @ManyToOne
    @JoinColumn(name = "author_id", nullable = false)
    private Profile author;

    @ManyToOne
    @JoinColumn(name = "supervisor_id")
    private Profile supervisor;

    @ManyToMany
    @JoinTable(
            name = "crm_project_curators",
            joinColumns = @JoinColumn(name = "project_id"),
            inverseJoinColumns = @JoinColumn(name = "profile_id")
    )
    private Set<Profile> curators;

    @ManyToMany
    @JoinTable(
            name = "crm_project_students",
            joinColumns = @JoinColumn(name = "project_id"),
            inverseJoinColumns = @JoinColumn(name = "profile_id")
    )
    private Set<Profile> students;

    @Column(length = 100)
    private String link;

    @Column(nullable = false)
    private LocalDate start;

    private LocalDate end;

    @Override
    public String toString() {
        return name;
    }
}
