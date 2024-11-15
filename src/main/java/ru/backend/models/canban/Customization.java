package ru.backend.models.canban;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
@Table(name = "canban_customization")
public class Customization {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "photo", length = 100, nullable = false)
    private String photo;

    @ManyToOne
    @JoinColumn(name = "task_id", nullable = false)
    private Task task;

    public Customization() {}

    public Customization(String photo, Task task) {
        this.photo = photo;
        this.task = task;
    }

}

