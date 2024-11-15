package ru.backend.models.crm;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Getter
@Setter
@Table(name = "crm_app_review")
public class AppReview {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "application_id", nullable = false)
    private Application application;

    @Column(nullable = false)
    private boolean isApproved;

    @Column(nullable = false, length = 1000)
    private String comment;

    @Column(nullable = false)
    private int testCount;

    @Column(nullable = false)
    private LocalDateTime dateTime;

}
