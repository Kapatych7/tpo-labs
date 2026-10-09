plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "ru.tpo.notes"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "ru.tpo.notes"
        minSdk = 24
        targetSdk = 37
        versionCode = 1
        versionName = "1.0"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(libs.appcompat)
    implementation(libs.material)
}
