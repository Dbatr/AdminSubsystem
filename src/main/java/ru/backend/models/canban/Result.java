package ru.backend.models.canban;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
@Table(name = "canban_result")
public class Result {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "text", nullable = false)
    private String text;

    @Column(name = "file", length = 100)
    private String file;

    @ManyToOne
    @JoinColumn(name = "task_id", nullable = false)
    private Task task;

    public Result() {}

    public Result(String text, String file, Task task) {
        this.text = text;
        this.file = file;
        this.task = task;
    }

}

