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
import ru.backend.auth.models.RefreshToken;
import ru.backend.auth.models.User;
import ru.backend.auth.models.UserProfile;
import ru.backend.auth.repositories.UserProfileRepository;
import ru.backend.auth.services.AuthService;
import ru.backend.auth.services.JwtService;
import ru.backend.auth.services.RefreshTokenService;
import ru.backend.auth.utils.*;

import java.util.Optional;

@Tag(name = "Аутентификация")
@RestController
@RequestMapping("/api/v1/auth/")
public class AuthController {

    private final AuthService authService;
    private final RefreshTokenService refreshTokenService;
    private final JwtService jwtService;

    private final UserProfileRepository userProfileRepository;

    public AuthController(AuthService authService, RefreshTokenService refreshTokenService, JwtService jwtService, UserProfileRepository userProfileRepository) {
        this.authService = authService;
        this.refreshTokenService = refreshTokenService;
        this.jwtService = jwtService;
        this.userProfileRepository = userProfileRepository;
    }

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
    public ResponseEntity<UserProfile> updateUserProfile(@RequestParam("token") String token, @RequestBody UserProfileUpdateRequest userProfileUpdateRequest) {
        String email = jwtService.extractUsername(token);

        if (email == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        User user = authService.getUserByEmail(email);

        UserProfile userProfile = user.getUserProfile();

        // Заполняем данные профиля
        userProfile.setName(userProfileUpdateRequest.getName());
        userProfile.setSurname(userProfileUpdateRequest.getSurname());
        userProfile.setPatronymic(userProfileUpdateRequest.getPatronymic());
        userProfile.setPhoneNumber(userProfileUpdateRequest.getPhoneNumber());
        userProfile.setDateOfBirth(userProfileUpdateRequest.getDateOfBirth());
        userProfile.setProfilePicture(userProfileUpdateRequest.getProfilePicture());
        userProfile.setUniversity(userProfileUpdateRequest.getUniversity());
        userProfile.setCourse(userProfileUpdateRequest.getCourse());
        userProfile.setSpeciality(userProfileUpdateRequest.getSpeciality());

        // Сохраняем обновленный профиль
        userProfileRepository.save(userProfile);

        return ResponseEntity.ok(userProfile);
    }

    @Operation(summary = "Получение информации о профиле пользователя", description = "Возвращает информацию о профиле пользователя для авторизованного пользователя")
    @ApiResponses(value = {
            @ApiResponse(responseCode = "200", description = "Информация о профиле пользователя успешно получена",
                    content = @Content(schema = @Schema(implementation = UserProfile.class))),
            @ApiResponse(responseCode = "401", description = "Не авторизован"),
            @ApiResponse(responseCode = "404", description = "Профиль пользователя не найден")
    })
    @GetMapping("/user/profile")
    public ResponseEntity<UserProfile> getUserProfileInfo(@RequestParam("token") String token) {
        String email = jwtService.extractUsername(token);

        if (email == null) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }

        User user = authService.getUserByEmail(email);
        if (user == null || user.getUserProfile() == null) {
            return ResponseEntity.notFound().build();
        }

        UserProfile userProfile = user.getUserProfile();
        return ResponseEntity.ok(userProfile);
    }
}
