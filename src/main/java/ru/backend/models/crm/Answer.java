package ru.backend.models.crm;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
@Table(name = "crm_answer")
public class Answer {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "question_id", nullable = false)
    private Question question;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private Profile user;

    @Column(name = "answer", nullable = false, length = 100)
    private String answer;

    @Column(name = "count", nullable = false)
    private Integer count;

}
