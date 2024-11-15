package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.canban.Tag;

@Repository
public interface TagRepository extends JpaRepository<Tag, Long> {
}
