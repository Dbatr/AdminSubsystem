package ru.backend.models.canban;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Setter
@Getter
@Entity
@Table(name = "canban_grade")
public class Grade {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "grade", nullable = false)
    private Integer grade;

    @Column(name = "review", nullable = false)
    private String review;

    @ManyToOne
    @JoinColumn(name = "result_id", nullable = false)
    private Result result;

    public Grade() {}

    public Grade(Integer grade, String review, Result result) {
        this.grade = grade;
        this.review = review;
        this.result = result;
    }

}

