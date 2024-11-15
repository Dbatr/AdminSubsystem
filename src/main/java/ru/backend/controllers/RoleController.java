//package ru.backend.controllers;
//
//import org.springframework.beans.factory.annotation.Autowired;
//import org.springframework.http.ResponseEntity;
//import org.springframework.web.bind.annotation.*;
//import ru.backend.dtos.RoleDTO;
//import ru.backend.models.crm.Role;
//import ru.backend.services.RoleService;
//
//import jakarta.validation.Valid;
//import java.util.List;
//import java.util.Optional;
//
//@RestController
//@RequestMapping("/api/roles")
//public class RoleController {
//    private final RoleService roleService;
//
//    @Autowired
//    public RoleController(RoleService roleService) {
//        this.roleService = roleService;
//    }
//
//    // Получение всех ролей
//    @GetMapping
//    public List<Role> getAllRoles() {
//        return roleService.getAllRoles();
//    }
//
//    // Получение роли по ID
//    @GetMapping("/{id}")
//    public ResponseEntity<Role> getRoleById(@PathVariable Integer id) {
//        Optional<Role> role = roleService.getRoleById(id);
//        return role.map(ResponseEntity::ok)
//                .orElseGet(() -> ResponseEntity.notFound().build());
//    }
//
//    // Добавление новой роли
//    @PostMapping
//    public ResponseEntity<Role> addRole(@Valid @RequestBody RoleDTO roleDTO) {
//        Role savedRole = roleService.addRole(roleDTO);
//        return ResponseEntity.ok(savedRole);
//    }
//
//    // Удаление роли по ID
//    @DeleteMapping("/{id}")
//    public ResponseEntity<Void> deleteRole(@PathVariable Integer id) {
//        if (roleService.getRoleById(id).isPresent()) {
//            roleService.deleteRole(id);
//            return ResponseEntity.noContent().build();
//        } else {
//            return ResponseEntity.notFound().build();
//        }
//    }
//}
