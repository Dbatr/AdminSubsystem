package ru.backend.models.crm;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import ru.backend.models.User;


@Entity
@Getter
@Setter
@Table(name = "crm_efficiency")
public class Efficiency {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Автоматическая генерация ID
    private Long id;

    @OneToOne
    @JoinColumn(name = "user_id", referencedColumnName = "id", nullable = false)
    private User user;

    @Column(nullable = false)
    private Integer count;

    @Column(nullable = false)
    private Float rating;

}
