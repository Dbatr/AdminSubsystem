package ru.backend.repositories;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import ru.backend.models.crm.Efficiency;

@Repository
public interface EfficiencyRepository extends JpaRepository<Efficiency, Long> {

}