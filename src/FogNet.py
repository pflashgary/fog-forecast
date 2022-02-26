from tensorflow.keras.models import Model
from tensorflow.keras import Input
from tensorflow.keras.layers import concatenate
from tensorflow.keras.layers import BatchNormalization, Dense, Dropout
from tensorflow.keras.layers import Conv3D, GlobalAveragePooling3D
from tensorflow.keras.layers import PReLU
import FogNetConfig


class FogNet:
    def __init__(self, stack_shape, filters, dropout, num_classes):

        self.num_classes = num_classes
        self.filters = filters
        self.dropout = dropout
        self.input_PhG1 = Input(stack_shape["PhG1"])  # 32*32*c1
        self.input_PhG2 = Input(stack_shape["PhG2"])  # 32*32*c2
        self.input_PhG3 = Input(stack_shape["PhG3"])  # 32*32*c3
        self.input_PhG4 = Input(stack_shape["PhG4"])  # 32*32*c4

    def BuildModel(self):
        # ===================================Group1 ===========================================
        NAM_G1_Depth = self.input_PhG1.shape[3]

        NAM_G1_Dense = FogNetConfig.SpectralDenseBlock(self.input_PhG1)
        NAM_Spectral_A_G1 = Conv3D(
            filters=self.filters, kernel_size=(1, 1, NAM_G1_Depth)
        )(
            NAM_G1_Dense
        )  ### <--------
        NAM_Spectral_A_G1 = BatchNormalization()(NAM_Spectral_A_G1)
        NAM_Spectral_A_G1 = PReLU()(NAM_Spectral_A_G1)
        NAM_Spectral_A_G1 = FogNetConfig.SpectralAttentionBlock(
            NAM_Spectral_A_G1, self.filters
        )

        NAM_Spatial_G1 = FogNetConfig.SpatialDenseBlock(NAM_Spectral_A_G1)
        NAM_Spatial_A_G1 = FogNetConfig.SpatialAttentionBlock(NAM_Spatial_G1)

        # ===================================Group2 ===========================================
        NAM_G2_Depth = self.input_PhG2.shape[3]

        NAM_G2_Dense = FogNetConfig.SpectralDenseBlock(self.input_PhG2)
        NAM_Spectral_A_G2 = Conv3D(
            filters=self.filters, kernel_size=(1, 1, NAM_G2_Depth)
        )(NAM_G2_Dense)
        NAM_Spectral_A_G2 = BatchNormalization()(NAM_Spectral_A_G2)
        NAM_Spectral_A_G2 = PReLU()(NAM_Spectral_A_G2)
        NAM_Spectral_A_G2 = FogNetConfig.SpectralAttentionBlock(
            NAM_Spectral_A_G2, self.filters
        )

        NAM_Spatial_G2 = FogNetConfig.SpatialDenseBlock(NAM_Spectral_A_G2)
        NAM_Spatial_A_G2 = FogNetConfig.SpatialAttentionBlock(NAM_Spatial_G2)

        # ===================================Group3 ===========================================
        NAM_G3_Depth = self.input_PhG3.shape[3]

        NAM_G3_Dense = FogNetConfig.SpectralDenseBlock(self.input_PhG3)
        NAM_Spectral_A_G3 = Conv3D(
            filters=self.filters, kernel_size=(1, 1, NAM_G3_Depth)
        )(NAM_G3_Dense)
        NAM_Spectral_A_G3 = BatchNormalization()(NAM_Spectral_A_G3)
        NAM_Spectral_A_G3 = PReLU()(NAM_Spectral_A_G3)
        NAM_Spectral_A_G3 = FogNetConfig.SpectralAttentionBlock(
            NAM_Spectral_A_G3, self.filters
        )

        NAM_Spatial_G3 = FogNetConfig.SpatialDenseBlock(NAM_Spectral_A_G3)
        NAM_Spatial_A_G3 = FogNetConfig.SpatialAttentionBlock(NAM_Spatial_G3)

        # ===================================Group4 ===========================================
        NAM_G4_Depth = self.input_PhG4.shape[3]

        NAM_G4_Dense = FogNetConfig.SpectralDenseBlock(self.input_PhG4)
        NAM_Spectral_A_G4 = Conv3D(
            filters=self.filters, kernel_size=(1, 1, NAM_G4_Depth)
        )(NAM_G4_Dense)
        NAM_Spectral_A_G4 = BatchNormalization()(NAM_Spectral_A_G4)
        NAM_Spectral_A_G4 = PReLU()(NAM_Spectral_A_G4)
        NAM_Spectral_A_G4 = FogNetConfig.SpectralAttentionBlock(
            NAM_Spectral_A_G4, self.filters
        )

        NAM_Spatial_G4 = FogNetConfig.SpatialDenseBlock(NAM_Spectral_A_G4)
        NAM_Spatial_A_G4 = FogNetConfig.SpatialAttentionBlock(NAM_Spatial_G4)

        # ===================================Group1 ===========================================
        NAM_Spectral = concatenate(
            [
                NAM_Spectral_A_G1,
                NAM_Spectral_A_G2,
                NAM_Spectral_A_G3,
                NAM_Spectral_A_G4,
            ],
            axis=3,
        )
        NAM_Spectral_Multi = FogNetConfig.NAMDilationBlock(NAM_Spectral)
        GLOBAL_NAM_Spectral_Multi = GlobalAveragePooling3D()(NAM_Spectral_Multi)
        GLOBAL_NAM_Spectral_Multi = Dropout(self.dropout)(
            GLOBAL_NAM_Spectral_Multi
        )  # defult = 0.4

        NAM_Spatial = concatenate(
            [
                NAM_Spatial_A_G1,
                NAM_Spatial_A_G2,
                NAM_Spatial_A_G3,
                NAM_Spatial_A_G4,
            ],
            axis=3,
        )
        NAM_Spatial_Multi = FogNetConfig.NAMDilationBlock(NAM_Spatial)
        GLOBAL_NAM_Satial_Multi = GlobalAveragePooling3D()(NAM_Spatial_Multi)
        GLOBAL_NAM_Satial_Multi = Dropout(self.dropout)(
            GLOBAL_NAM_Satial_Multi
        )  # defult = 0.4
        # Concatenate Spectral ana Spatial features
        FinalConcat = concatenate(
            [GLOBAL_NAM_Spectral_Multi, GLOBAL_NAM_Satial_Multi], axis=1
        )

        # prediction
        prediction = Dense(units=self.num_classes, activation="softmax")(FinalConcat)
        model = Model(
            inputs=[
                self.input_PhG1,
                self.input_PhG2,
                self.input_PhG3,
                self.input_PhG4,
            ],
            outputs=prediction,
        )

        return model
