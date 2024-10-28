package ru.backend.auth.utils;

import lombok.Data;

import java.time.LocalDate;

@Data
public class UserProfileUpdateRequest {

    private String name;

    private String surname;

    private String patronymic;

    private String phoneNumber;

    private LocalDate dateOfBirth;

    private String profilePicture;

    private String university;

    private String course;

    private String speciality;
}
