package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.canban.Comment;

@Repository
public interface CommentRepository extends JpaRepository<Comment, Long> {
}
