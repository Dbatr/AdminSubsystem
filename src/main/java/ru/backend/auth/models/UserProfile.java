package ru.backend.auth.models;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Data;

import java.time.LocalDate;

@Data
@Entity
@Table(name = "user_profiles")
public class UserProfile {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;

    private String surname;

    private String patronymic;

    private String phoneNumber;

    private LocalDate dateOfBirth;

    private String profilePicture;

    private String university;

    private String course;

    private String speciality;

    @JsonIgnore
    @OneToOne(mappedBy = "userProfile")
    private User user;
}
