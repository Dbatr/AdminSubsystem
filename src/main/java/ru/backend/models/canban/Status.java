package ru.backend.models.canban;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;
import ru.backend.models.crm.Direction;

@Setter
@Getter
@Entity
@Table(name = "canban_status")
public class Status {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "name", length = 256, nullable = false)
    private String name;

    @ManyToOne
    @JoinColumn(name = "direction_id", nullable = false)
    private Direction direction;

    public Status() {}

    public Status(String name, Direction direction) {
        this.name = name;
        this.direction = direction;
    }

}

