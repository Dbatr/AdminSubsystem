package ru.backend.auth.utils;

import lombok.Data;

import java.time.LocalDate;
import java.util.Set;

@Data
public class UserProfileUpdateRequest {

    private String name;
    private String surname;
    private String patronymic;
    private String photo;
    private String telegram;
    private String email;
    private String phoneNumber;
    private LocalDate dateOfBirth;
    private String university;
    private Integer course;
    private Set<Integer> skillIds;
}
