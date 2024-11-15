package ru.backend.models.canban;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import ru.backend.models.crm.Direction;
import ru.backend.models.crm.Profile;

import java.time.LocalDateTime;
import java.util.Set;


@Setter
@Getter
@Entity
@Table(name = "canban_task")
public class Task {

    // Getters и Setters
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", length = 256, nullable = false)
    private String name;

    @Column(name = "description", columnDefinition = "TEXT", nullable = false)
    private String description;

    @Column(name = "datetime", nullable = false)
    private LocalDateTime datetime;

    @Column(name = "deadline")
    private LocalDateTime deadline;

    @ManyToOne
    @JoinColumn(name = "author_id", nullable = false)
    private Profile author;

    @ManyToOne
    @JoinColumn(name = "direction_id", nullable = false)
    private Direction direction;

    @ManyToMany
    @JoinTable(
            name = "canban_task_responsible_users",
            joinColumns = @JoinColumn(name = "task_id"),
            inverseJoinColumns = @JoinColumn(name = "profile_id")
    )
    private Set<Profile> responsibleUsers;

    // Конструкторы
    public Task() {}

    public Task(String name, String description, LocalDateTime datetime, Profile author, Direction direction) {
        this.name = name;
        this.description = description;
        this.datetime = datetime;
        this.author = author;
        this.direction = direction;
    }

}
