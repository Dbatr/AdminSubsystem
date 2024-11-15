package ru.backend.controllers;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import ru.backend.auth.services.AuthService;
import ru.backend.auth.services.JwtService;
import ru.backend.auth.services.RefreshTokenService;
import ru.backend.auth.utils.*;
import ru.backend.models.RefreshToken;
import ru.backend.models.User;
import ru.backend.models.crm.Profile;
import ru.backend.models.crm.Skill;
import ru.backend.repositories.ProfileRepository;
import ru.backend.repositories.SkillRepository;

import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

@Tag(name = "Аутентификация")
@RestController
@RequestMapping("/api/v1/auth/")
public class AuthController {

    private final AuthService authService;
    private final RefreshTokenService refreshTokenService;
    private final JwtService jwtService;

    private final ProfileRepository userProfileRepository;
    private final SkillRepository skillRepository;

    public AuthController(AuthService authService, RefreshTokenService refreshTokenService, JwtService jwtService, ProfileRepository userProfileRepository, SkillRepository skillRepository) {
        this.authService = authService;
        this.refreshTokenService = refreshTokenService;
        this.jwtService = jwtService;
        this.userProfileRepository = userProfileRepository;
        this.skillRepository = skillRepository;
    }


    // Todo не добавляется почта в профиль при регистрации
    @Operation(summary = "Регистрация нового пользователя", description = "Регистрация нового пользователя с предоставленными данными")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Пользователь успешно зарегистрирован",
                    content = @Content(schema = @Schema(implementation = AuthResponse.class))),
            @ApiResponse(responseCode = "400", description = "Неверные входные данные")
    })
    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(@RequestBody RegisterRequest registerRequest) {
        return ResponseEntity.ok(authService.register(registerRequest));
    }

    @Operation(summary = "Вход пользователя", description = "Вход пользователя с предоставленными учетными данными")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Пользователь успешно вошел в систему",
                    content = @Content(schema = @Schema(implementation = AuthResponse.class))),
            @ApiResponse(responseCode = "400", description = "Неверные учетные данные")
    })
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(@RequestBody LoginRequest loginRequest) {
        return ResponseEntity.ok(authService.login(loginRequest));
    }

    @Operation(summary = "Обновление токена доступа", description = "Обновление токена доступа с использованием предоставленного токена обновления")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Токен доступа успешно обновлен",
                    content = @Content(schema = @Schema(implementation = AuthResponse.class))),
            @ApiResponse(responseCode = "400", description = "Неверный токен обновления")
    })
    @PostMapping("/refresh")
    public ResponseEntity<AuthResponse> refreshToken(@RequestBody RefreshTokenRequest refreshTokenRequest) {

        RefreshToken refreshToken = refreshTokenService.verifyRefreshToken(refreshTokenRequest.getRefreshToken());
        User user = refreshToken.getUser();

        String accessToken = jwtService.generateToken(user);

        return ResponseEntity.ok(AuthResponse.builder()
                .accessToken(accessToken)
                .refreshToken(refreshToken.getRefreshToken())
                .build());
    }

    @Operation(summary = "Получение информации о пользователе", description = "Возвращает имя, имя пользователя, email и роль пользователя для авторизованного пользователя")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Информация о пользователе успешно получена",
                    content = @Content(schema = @Schema(implementation = AccountDetails.class))),
            @ApiResponse(responseCode = "401", description = "Не авторизован"),
            @ApiResponse(responseCode = "404", description = "Пользователь не найден")
    })
    @GetMapping("/user")
    public ResponseEntity<AccountDetails> getUserInfo(@RequestParam("token") String token) {
        String email = jwtService.extractUsername(token);

        if (email == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        Optional<User> userOptional = Optional.ofNullable(authService.getUserByEmail(email));
        if (userOptional.isEmpty()) {
            return ResponseEntity.notFound().build();
        }
        var user = userOptional.get();

        AccountDetails accountDetails = new AccountDetails();
        accountDetails.setEmail(user.getEmail());
        accountDetails.setRole(user.getRole().name());
        return ResponseEntity.ok(accountDetails);
    }

    @Operation(summary = "Обновление профиля пользователя", description = "Обновляет данные профиля пользователя")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Профиль успешно обновлен"),
            @ApiResponse(responseCode = "401", description = "Не авторизован"),
            @ApiResponse(responseCode = "404", description = "Пользователь не найден")
    })
    @PutMapping("/user/profile")
    public ResponseEntity<Profile> updateUserProfile(
            @RequestParam("token") String token,
            @RequestBody UserProfileUpdateRequest userProfileUpdateRequest) {

        String email = jwtService.extractUsername(token);

        if (email == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        User user = authService.getUserByEmail(email);
        if (user == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        Profile userProfile = user.getProfile();
        if (userProfile == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        // Заполняем данные профиля
        userProfile.setName(userProfileUpdateRequest.getName());
        userProfile.setSurname(userProfileUpdateRequest.getSurname());
        userProfile.setPatronymic(userProfileUpdateRequest.getPatronymic());
        userProfile.setPhoto(userProfileUpdateRequest.getPhoto());
        userProfile.setTelegram(userProfileUpdateRequest.getTelegram());
        userProfile.setEmail(userProfileUpdateRequest.getEmail());
        userProfile.setUniversity(userProfileUpdateRequest.getUniversity());
        userProfile.setCourse(userProfileUpdateRequest.getCourse());

        // Обновляем навыки профиля, если переданы skillIds
        if (userProfileUpdateRequest.getSkillIds() != null && !userProfileUpdateRequest.getSkillIds().isEmpty()) {
            Set<Skill> skills = new HashSet<>(skillRepository.findAllById(userProfileUpdateRequest.getSkillIds()));
            userProfile.setSkills(skills);
        }

        // Сохраняем обновленный профиль
        userProfileRepository.save(userProfile);

        return ResponseEntity.ok(userProfile);
    }

    @Operation(summary = "Получение информации о профиле пользователя", description = "Возвращает информацию о профиле пользователя для авторизованного пользователя")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Информация о профиле пользователя успешно получена",
                    content = @Content(schema = @Schema(implementation = Profile.class))),
            @ApiResponse(responseCode = "401", description = "Не авторизован"),
            @ApiResponse(responseCode = "404", description = "Профиль пользователя не найден")
    })
    @GetMapping("/user/profile")
    public ResponseEntity<Profile> getUserProfileInfo(@RequestParam("token") String token) {
        String email = jwtService.extractUsername(token);

        if (email == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        User user = authService.getUserByEmail(email);
        if (user == null || user.getProfile() == null) {
            return ResponseEntity.notFound().build();
        }

        Profile userProfile = user.getProfile();
        return ResponseEntity.ok(userProfile);
    }
}