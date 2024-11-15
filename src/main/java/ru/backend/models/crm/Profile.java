package ru.backend.models.crm;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import ru.backend.models.User;

import java.util.Set;

@Entity
@Getter
@Setter
@Table(name = "crm_profile")
public class Profile {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @JsonIgnore
    @OneToOne
    @JoinColumn(name = "author_id", referencedColumnName = "id")
    private User author;

    @Column(length = 100)
    private String photo;

    @Column(length = 100)
    private String telegram;

    @Column(length = 100)
    private String email;

    @Column(length = 100)
    private String surname;

    @Column(length = 100)
    private String name;

    @Column(length = 100)
    private String patronymic;

    private Integer course;

    @Column(length = 100)
    private String university;

    @ManyToMany
    @JoinTable(
            name = "crm_profile_skills",
            joinColumns = @JoinColumn(name = "profile_id", referencedColumnName = "author_id"),
            inverseJoinColumns = @JoinColumn(name = "skill_id", referencedColumnName = "id")
    )
    private Set<Skill> skills;

    @Override
    public String toString() {
        return surname + " " + name + " " + patronymic;
    }
}
