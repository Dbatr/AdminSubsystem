package ru.backend.models.canban;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
@Table(name = "canban_tag")
public class Tag {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", length = 256, nullable = false)
    private String name;

    @ManyToOne
    @JoinColumn(name = "task_id", nullable = false)
    private Task task;

    public Tag() {}

    public Tag(String name, Task task) {
        this.name = name;
        this.task = task;
    }

}

