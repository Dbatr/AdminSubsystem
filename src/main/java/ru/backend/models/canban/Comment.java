package ru.backend.models.canban;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import ru.backend.models.crm.Profile;

@Setter
@Getter
@Entity
@Table(name = "canban_comment")
public class Comment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "content", nullable = false)
    private String content;

    @ManyToOne
    @JoinColumn(name = "author_id", nullable = false)
    private Profile author;

    @ManyToOne
    @JoinColumn(name = "task_id", nullable = false)
    private Task task;

    public Comment() {}

    public Comment(String content, Profile author, Task task) {
        this.content = content;
        this.author = author;
        this.task = task;
    }

}

