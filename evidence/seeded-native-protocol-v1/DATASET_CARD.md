---
dataset_info:
- config_name: default
  features:
  - name: metrics.id
    dtype: string
  - name: metrics.json
    dtype: string
  - name: metrics.aspect_ratio
    dtype: float64
  - name: metrics.aspect_ratio_over_edge_rotational_transform
    dtype: float64
  - name: metrics.average_triangularity
    dtype: float64
  - name: metrics.axis_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.axis_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.edge_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.edge_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.flux_compression_in_regions_of_bad_curvature
    dtype: float64
  - name: metrics.max_elongation
    dtype: float64
  - name: metrics.minimum_normalized_magnetic_gradient_scale_length
    dtype: float64
  - name: metrics.qi
    dtype: float64
  - name: metrics.vacuum_well
    dtype: float64
  - name: boundary.json
    dtype: string
  - name: boundary.is_stellarator_symmetric
    dtype: bool
  - name: boundary.n_field_periods
    dtype: int64
  - name: boundary.n_periodicity
    dtype: int64
  - name: boundary.r_cos
    sequence:
      sequence: float64
  - name: boundary.r_sin
    dtype: 'null'
  - name: boundary.z_cos
    dtype: 'null'
  - name: boundary.z_sin
    sequence:
      sequence: float64
  - name: omnigenous_field_and_targets.id
    dtype: string
  - name: omnigenous_field_and_targets.json
    dtype: string
  - name: omnigenous_field_and_targets.aspect_ratio
    dtype: float64
  - name: omnigenous_field_and_targets.major_radius
    dtype: float64
  - name: omnigenous_field_and_targets.max_elongation
    dtype: float64
  - name: omnigenous_field_and_targets.omnigenous_field.modB_spline_knot_coefficients
    sequence:
      sequence: float64
  - name: omnigenous_field_and_targets.omnigenous_field.n_field_periods
    dtype: int64
  - name: omnigenous_field_and_targets.omnigenous_field.poloidal_winding
    dtype: int64
  - name: omnigenous_field_and_targets.omnigenous_field.torodial_winding
    dtype: int64
  - name: omnigenous_field_and_targets.omnigenous_field.x_lmn
    sequence:
      sequence:
        sequence: float64
  - name: omnigenous_field_and_targets.rotational_transform
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.id
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.json
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.equilibrium_settings.check_orientation
    dtype: bool
  - name: desc_omnigenous_field_optimization_settings.equilibrium_settings.max_poloidal_mode
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.equilibrium_settings.max_toroidal_mode
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.equilibrium_settings.psi
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.aspect_ratio
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.elongation
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.is_iota_positive
    dtype: bool
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.is_stellarator_symmetric
    dtype: bool
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.major_radius
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.max_elongation
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.max_poloidal_mode
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.max_toroidal_mode
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.mirror_ratio
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.n_field_periods
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.rotational_transform
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.initial_guess_settings.torsion
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.aspect_ratio_settings.name
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.objective_settings.aspect_ratio_settings.target_kind
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.objective_settings.aspect_ratio_settings.weight
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.elongation_settings.name
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.objective_settings.elongation_settings.target_kind
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.objective_settings.elongation_settings.weight
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.omnigenity_settings.eq_lcfs_grid_M_factor
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.omnigenity_settings.eq_lcfs_grid_N_factor
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.omnigenity_settings.eq_lcfs_grid_rho
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.omnigenity_settings.eta_weight
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.omnigenity_settings.name
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.objective_settings.omnigenity_settings.weight
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.objective_settings.rotational_transform_settings.name
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.objective_settings.rotational_transform_settings.target_kind
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.objective_settings.rotational_transform_settings.weight
    dtype: float64
  - name: desc_omnigenous_field_optimization_settings.optimizer_settings.maxiter
    dtype: int64
  - name: desc_omnigenous_field_optimization_settings.optimizer_settings.name
    dtype: string
  - name: desc_omnigenous_field_optimization_settings.optimizer_settings.verbose
    dtype: int64
  - name: vmec_omnigenous_field_optimization_settings.id
    dtype: string
  - name: vmec_omnigenous_field_optimization_settings.json
    dtype: string
  - name: vmec_omnigenous_field_optimization_settings.gradient_based_relative_objectives_tolerance
    dtype: float64
  - name: vmec_omnigenous_field_optimization_settings.gradient_free_budget_per_design_variable
    dtype: int64
  - name: vmec_omnigenous_field_optimization_settings.gradient_free_max_time
    dtype: int64
  - name: vmec_omnigenous_field_optimization_settings.gradient_free_optimization_hypercube_bounds
    dtype: float64
  - name: vmec_omnigenous_field_optimization_settings.infinity_norm_spectrum_scaling
    dtype: float64
  - name: vmec_omnigenous_field_optimization_settings.max_poloidal_mode
    dtype: int64
  - name: vmec_omnigenous_field_optimization_settings.max_toroidal_mode
    dtype: int64
  - name: vmec_omnigenous_field_optimization_settings.n_inner_optimizations
    dtype: int64
  - name: vmec_omnigenous_field_optimization_settings.use_continuation_method_in_fourier_space
    dtype: bool
  - name: vmec_omnigenous_field_optimization_settings.verbose
    dtype: bool
  - name: qp_init_omnigenous_field_optimization_settings.id
    dtype: string
  - name: qp_init_omnigenous_field_optimization_settings.json
    dtype: string
  - name: qp_init_omnigenous_field_optimization_settings.aspect_ratio
    dtype: float64
  - name: qp_init_omnigenous_field_optimization_settings.elongation
    dtype: float64
  - name: qp_init_omnigenous_field_optimization_settings.is_iota_positive
    dtype: bool
  - name: qp_init_omnigenous_field_optimization_settings.is_stellarator_symmetric
    dtype: bool
  - name: qp_init_omnigenous_field_optimization_settings.major_radius
    dtype: float64
  - name: qp_init_omnigenous_field_optimization_settings.mirror_ratio
    dtype: float64
  - name: qp_init_omnigenous_field_optimization_settings.n_field_periods
    dtype: int64
  - name: qp_init_omnigenous_field_optimization_settings.torsion
    dtype: float64
  - name: nae_init_omnigenous_field_optimization_settings.id
    dtype: string
  - name: nae_init_omnigenous_field_optimization_settings.json
    dtype: string
  - name: nae_init_omnigenous_field_optimization_settings.aspect_ratio
    dtype: float64
  - name: nae_init_omnigenous_field_optimization_settings.max_elongation
    dtype: float64
  - name: nae_init_omnigenous_field_optimization_settings.max_poloidal_mode
    dtype: int64
  - name: nae_init_omnigenous_field_optimization_settings.max_toroidal_mode
    dtype: int64
  - name: nae_init_omnigenous_field_optimization_settings.mirror_ratio
    dtype: float64
  - name: nae_init_omnigenous_field_optimization_settings.n_field_periods
    dtype: int64
  - name: nae_init_omnigenous_field_optimization_settings.rotational_transform
    dtype: float64
  - name: misc.vmecpp_wout_id
    dtype: string
  - name: misc.has_optimize_boundary_omnigenity_vmec_error
    dtype: bool
  - name: misc.has_optimize_boundary_omnigenity_desc_error
    dtype: bool
  - name: misc.has_generate_qp_initialization_from_targets_error
    dtype: bool
  - name: misc.has_generate_nae_initialization_from_targets_error
    dtype: bool
  - name: misc.has_neurips_2025_forward_model_error
    dtype: bool
  - name: plasma_config_id
    dtype: string
  splits:
  - name: train
    num_bytes: 1240651097.3174775
    num_examples: 182222
  download_size: 610201645
  dataset_size: 1240651097.3174775
- config_name: finite_beta_1pct
  features:
  - name: metrics.id
    dtype: string
  - name: metrics.json
    dtype: string
  - name: metrics.aspect_ratio
    dtype: float64
  - name: metrics.aspect_ratio_over_edge_rotational_transform
    dtype: float64
  - name: metrics.average_triangularity
    dtype: float64
  - name: metrics.axis_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.axis_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.edge_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.edge_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.flux_compression_in_regions_of_bad_curvature
    dtype: float64
  - name: metrics.max_elongation
    dtype: float64
  - name: metrics.minimum_normalized_magnetic_gradient_scale_length
    dtype: float64
  - name: metrics.qi
    dtype: float64
  - name: metrics.vacuum_well
    dtype: float64
  - name: misc.vmecpp_wout_id
    dtype: string
  - name: misc.source_plasma_config_id
    dtype: string
  - name: misc.has_neurips_2025_forward_model_error
    dtype: bool
  - name: plasma_config_id
    dtype: string
  splits:
  - name: train
    num_bytes: 76508664.04284965
    num_examples: 112804
  download_size: 52556502
  dataset_size: 76508664.04284965
- config_name: finite_beta_2pct
  features:
  - name: metrics.id
    dtype: string
  - name: metrics.json
    dtype: string
  - name: metrics.aspect_ratio
    dtype: float64
  - name: metrics.aspect_ratio_over_edge_rotational_transform
    dtype: float64
  - name: metrics.average_triangularity
    dtype: float64
  - name: metrics.axis_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.axis_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.edge_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.edge_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.flux_compression_in_regions_of_bad_curvature
    dtype: float64
  - name: metrics.max_elongation
    dtype: float64
  - name: metrics.minimum_normalized_magnetic_gradient_scale_length
    dtype: float64
  - name: metrics.qi
    dtype: float64
  - name: metrics.vacuum_well
    dtype: float64
  - name: misc.vmecpp_wout_id
    dtype: string
  - name: misc.source_plasma_config_id
    dtype: string
  - name: misc.has_neurips_2025_forward_model_error
    dtype: bool
  - name: plasma_config_id
    dtype: string
  splits:
  - name: train
    num_bytes: 47402708.67692375
    num_examples: 82722
  download_size: 38593722
  dataset_size: 47402708.67692375
- config_name: finite_beta_3pct
  features:
  - name: metrics.id
    dtype: string
  - name: metrics.json
    dtype: string
  - name: metrics.aspect_ratio
    dtype: float64
  - name: metrics.aspect_ratio_over_edge_rotational_transform
    dtype: float64
  - name: metrics.average_triangularity
    dtype: float64
  - name: metrics.axis_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.axis_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.edge_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.edge_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.flux_compression_in_regions_of_bad_curvature
    dtype: float64
  - name: metrics.max_elongation
    dtype: float64
  - name: metrics.minimum_normalized_magnetic_gradient_scale_length
    dtype: float64
  - name: metrics.qi
    dtype: float64
  - name: metrics.vacuum_well
    dtype: float64
  - name: misc.vmecpp_wout_id
    dtype: string
  - name: misc.source_plasma_config_id
    dtype: string
  - name: misc.has_neurips_2025_forward_model_error
    dtype: bool
  - name: plasma_config_id
    dtype: string
  splits:
  - name: train
    num_bytes: 25395079.54877086
    num_examples: 55448
  download_size: 25947395
  dataset_size: 25395079.54877086
- config_name: finite_beta_4pct
  features:
  - name: metrics.id
    dtype: string
  - name: metrics.json
    dtype: string
  - name: metrics.aspect_ratio
    dtype: float64
  - name: metrics.aspect_ratio_over_edge_rotational_transform
    dtype: float64
  - name: metrics.average_triangularity
    dtype: float64
  - name: metrics.axis_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.axis_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.edge_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.edge_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.flux_compression_in_regions_of_bad_curvature
    dtype: float64
  - name: metrics.max_elongation
    dtype: float64
  - name: metrics.minimum_normalized_magnetic_gradient_scale_length
    dtype: float64
  - name: metrics.qi
    dtype: float64
  - name: metrics.vacuum_well
    dtype: float64
  - name: misc.vmecpp_wout_id
    dtype: string
  - name: misc.source_plasma_config_id
    dtype: string
  - name: misc.has_neurips_2025_forward_model_error
    dtype: bool
  - name: plasma_config_id
    dtype: string
  splits:
  - name: train
    num_bytes: 13509704.764567751
    num_examples: 36444
  download_size: 17086365
  dataset_size: 13509704.764567751
- config_name: finite_beta_5pct
  features:
  - name: metrics.id
    dtype: string
  - name: metrics.json
    dtype: string
  - name: metrics.aspect_ratio
    dtype: float64
  - name: metrics.aspect_ratio_over_edge_rotational_transform
    dtype: float64
  - name: metrics.average_triangularity
    dtype: float64
  - name: metrics.axis_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.axis_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.edge_magnetic_mirror_ratio
    dtype: float64
  - name: metrics.edge_rotational_transform_over_n_field_periods
    dtype: float64
  - name: metrics.flux_compression_in_regions_of_bad_curvature
    dtype: float64
  - name: metrics.max_elongation
    dtype: float64
  - name: metrics.minimum_normalized_magnetic_gradient_scale_length
    dtype: float64
  - name: metrics.qi
    dtype: float64
  - name: metrics.vacuum_well
    dtype: float64
  - name: misc.vmecpp_wout_id
    dtype: string
  - name: misc.source_plasma_config_id
    dtype: string
  - name: misc.has_neurips_2025_forward_model_error
    dtype: bool
  - name: plasma_config_id
    dtype: string
  splits:
  - name: train
    num_bytes: 8792377.219300479
    num_examples: 26729
  download_size: 12538180
  dataset_size: 8792377.219300479
- config_name: vmecpp_wout
  features:
  - name: plasma_config_id
    dtype: string
  - name: id
    dtype: string
  - name: json
    dtype: string
  splits:
  - name: train
    num_bytes: 1100757693175
    num_examples: 148292
  download_size: 956063943
  dataset_size: 1100757693175
- config_name: vmecpp_wout_finite_beta_1pct
  features:
  - name: plasma_config_id
    dtype: string
  - name: id
    dtype: string
  - name: json
    dtype: string
  splits:
  - name: train
    num_bytes: 1100757693175
    num_examples: 148292
  download_size: 956063943
  dataset_size: 1100757693175
- config_name: vmecpp_wout_finite_beta_2pct
  features:
  - name: plasma_config_id
    dtype: string
  - name: id
    dtype: string
  - name: json
    dtype: string
  splits:
  - name: train
    num_bytes: 1100757693175
    num_examples: 148292
  download_size: 956063943
  dataset_size: 1100757693175
- config_name: vmecpp_wout_finite_beta_3pct
  features:
  - name: plasma_config_id
    dtype: string
  - name: id
    dtype: string
  - name: json
    dtype: string
  splits:
  - name: train
    num_bytes: 1100757693175
    num_examples: 148292
  download_size: 956063943
  dataset_size: 1100757693175
- config_name: vmecpp_wout_finite_beta_4pct
  features:
  - name: plasma_config_id
    dtype: string
  - name: id
    dtype: string
  - name: json
    dtype: string
  splits:
  - name: train
    num_bytes: 1100757693175
    num_examples: 148292
  download_size: 956063943
  dataset_size: 1100757693175
- config_name: vmecpp_wout_finite_beta_5pct
  features:
  - name: plasma_config_id
    dtype: string
  - name: id
    dtype: string
  - name: json
    dtype: string
  splits:
  - name: train
    num_bytes: 1100757693175
    num_examples: 148292
  download_size: 956063943
  dataset_size: 1100757693175
configs:
- config_name: default
  data_files:
  - split: train
    path: data/train-*
- config_name: finite_beta_1pct
  data_files:
  - split: train
    path: finite_beta_1pct/train-*
- config_name: finite_beta_2pct
  data_files:
  - split: train
    path: finite_beta_2pct/train-*
- config_name: finite_beta_3pct
  data_files:
  - split: train
    path: finite_beta_3pct/train-*
- config_name: finite_beta_4pct
  data_files:
  - split: train
    path: finite_beta_4pct/train-*
- config_name: finite_beta_5pct
  data_files:
  - split: train
    path: finite_beta_5pct/train-*
- config_name: vmecpp_wout
  data_files:
  - split: train
    path: vmecpp_wout/part*
- config_name: vmecpp_wout_finite_beta_1pct
  data_files:
  - split: train
    path: vmecpp_wout_finite_beta_1pct/part*
- config_name: vmecpp_wout_finite_beta_2pct
  data_files:
  - split: train
    path: vmecpp_wout_finite_beta_2pct/part*
- config_name: vmecpp_wout_finite_beta_3pct
  data_files:
  - split: train
    path: vmecpp_wout_finite_beta_3pct/part*
- config_name: vmecpp_wout_finite_beta_4pct
  data_files:
  - split: train
    path: vmecpp_wout_finite_beta_4pct/part*
- config_name: vmecpp_wout_finite_beta_5pct
  data_files:
  - split: train
    path: vmecpp_wout_finite_beta_5pct/part*
license: mit
language:
- en
tags:
- physics
- fusion
- optimization
- neurips
pretty_name: ConStellaration
size_categories:
- 100K<n<1M
---
# Dataset Card for ConStellaration

<!-- Provide a quick summary of the dataset. -->

A dataset of diverse quasi-isodynamic (QI) stellarator boundary shapes with corresponding performance metrics and ideal magneto-hydrodynamic (MHD) equilibria, as well as settings for their generation.

The performance metrics and ideal MHD equilibria were evaluated under vacuum (default) and with plasma inside (finite beta).

## Dataset Details

### Dataset Description

<!-- Provide a longer summary of what this dataset is. -->

Stellarators are magnetic confinement devices that are being pursued to deliver steady-state carbon-free fusion energy. Their design involves a high-dimensional, constrained optimization problem that requires expensive physics simulations and significant domain expertise. Specifically, QI-stellarators are seen as a promising path to commercial fusion due to their intrinsic avoidance of current-driven disruptions. 

With the release of this dataset, we aim to lower the barrier for optimization and machine learning researchers to contribute to stellarator design, and to accelerate cross-disciplinary progress toward bringing fusion energy to the grid.

- **Curated by:** Proxima Fusion
- **License:** MIT

![Diagram of the computation of metrics of interest from a plasma boundary via the MHD equilibrium](assets/mhd_intro_v2.png)

### Dataset Sources

<!-- Provide the basic links for the dataset. -->

- **Repository:** https://huggingface.co/datasets/proxima-fusion/constellaration
- **Paper:** https://arxiv.org/abs/2506.19583
- **Code:** https://github.com/proximafusion/constellaration

## Dataset Structure

<!-- This section provides a description of the dataset fields, and additional information about the dataset structure such as criteria used to create the splits, relationships between data points, etc. -->

There are 6 tuples of datasets, one for each percentage of volume-averaged plasma inside the boundary:
<table>
  <tr>
    <th>Condition</th>
    <th>Boundaries, Metrics, Generation Settings, Misc</th>
    <th>Ideal MHD Equilibira</th>
  </tr>
  <tr>
    <th>Vacuum</th>
    <th>default</th>
    <th>vmecpp_wout</th>
  </tr>
  <tr>
    <th>1% Beta</th>
    <th>finte_beta_1pct</th>
    <th>vmecpp_wout_finite_beta_1pct</th>
  </tr>
  <tr>
    <th>2% Beta</th>
    <th>finte_beta_2pct</th>
    <th>vmecpp_wout_finite_beta_2pct</th>
  </tr>
  <tr>
    <th>3% Beta</th>
    <th>finte_beta_3pct</th>
    <th>vmecpp_wout_finite_beta_3pct</th>
  </tr>
  <tr>
    <th>4% Beta</th>
    <th>finte_beta_4pct</th>
    <th>vmecpp_wout_finite_beta_4pct</th>
  </tr>
  <tr>
    <th>5% Beta</th>
    <th>finte_beta_5pct</th>
    <th>vmecpp_wout_finite_beta_5pct</th>
  </tr>
</table>
<br>
Contents of datasets:
<table>
  <tr>
    <th style="border-right: 1px solid gray;">default</th>
    <th>vmecpp_wout</th>
  </tr>
  <tr>
    <td style="border-right: 1px solid gray;">
      Contains information about:
      <ul>
        <li>Plasma boundaries</li>
        <li>Ideal MHD metrics in vacuum</li>
        <li>Omnigenous field and targets, used as input for sampling of plasma boundaries</li>
        <li>Sampling settings for various methods (DESC, VMEC, QP initialization, Near-axis expansion)</li>
        <li>Miscellaneous information
          <ul>
            <li>the corresponding ideal MHD equilibrium ID in <b>vmecpp_wout</b></li>
            <li>errors that might have occurred during sampling or metrics computation.</li>
          </ul>
        </li>
      </ul>
    </td>
    <td>
      Contains:
      <ul>
        <li>For each plasma boundary in <b>default</b>, a JSON-string representation of the "WOut" file as obtained when running VMEC, initialized on the boundary.<br>The JSON representation can be converted to a VMEC2000 output file.</li>
        <li>The corresponding plasma configuration ID in <b>default</b></li>
      </ul>
    </td>
  </tr>
  <tr>
    <td colspan="2">
      The <b>default</b> (vacuum) subset above is special in the sense that it contains more information than the other subsets (finite betas) below. Those are derived from the <b>default</b> (vacuum) subset by setting for each plasma boundary the respective volume-averaged beta percentage and re-computing the performance metrics and ideal MHD equilibria:
    </td>
  </tr>
  <tr>
    <th style="border-right: 1px solid gray;">finite_beta_*pct</th>
    <th>vmecpp_wout_finite_beta_*pct</th>
  </tr>
  <tr>
    <td style="border-right: 1px solid gray;">
      Contains information about:
      <ul>
        <li>Ideal MHD metrics with plasma</li>
        <li>Miscellaneous information
          <ul>
            <li>the corresponding source plasma configuration ID in <b>default</b></li>
            <li>the corresponding ideal MHD equilibrium ID in <b>vmecpp_wout_finite_beta_*pct</b></li>
            <li>errors that might have occurred metrics computation.</li>
          </ul>
        </li>
      </ul>
    </td>
    <td>
      Same as <b>vmecpp_wout</b> above, corresponding to <b>finite_beta_*pct</b>
    </td>
  </tr>
</table>

For each of the components above there is an identifier column (ending with `.id`), a JSON column containing a JSON-string representation, as well as one column per leaf in the nested JSON structure (with `.` separating the keys on the JSON path to the respective leaf).

## Uses

Install Huggingface Datasets: `pip install datasets`

### Basic Usage
Load the dataset and convert to a Pandas Dataframe (here, `torch` is used as an example; install it with" `pip install torch`):
```python
import datasets
import torch
from pprint import pprint

ds = datasets.load_dataset(
    "proxima-fusion/constellaration",
    split="train",
    num_proc=4,
)
ds = ds.select_columns([c for c in ds.column_names
                        if c.startswith("boundary.")
                        or c.startswith("metrics.")])
ds = ds.filter(
    lambda x: x == 3,
    input_columns=["boundary.n_field_periods"],
    num_proc=4,
)
ml_ds = ds.remove_columns([
    "boundary.n_field_periods", "boundary.is_stellarator_symmetric",  # all same value
    "boundary.r_sin", "boundary.z_cos",  # empty
    "boundary.json", "metrics.json", "metrics.id",  # not needed
])

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch_ds = ml_ds.with_format("torch", device=device)  # other options: "jax", "tensorflow" etc.

for batch in torch.utils.data.DataLoader(torch_ds, batch_size=4, num_workers=4):
    pprint(batch)
    break
```
<div style="margin-left: 1em;">
<details>
<summary>Output</summary>

```python
{'boundary.r_cos': tensor([[[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  1.0000e+00,
          -6.5763e-02, -3.8500e-02,  2.2178e-03,  4.6007e-04],
         [-6.6648e-04, -1.0976e-02,  5.6475e-02,  1.4193e-02,  8.3476e-02,
          -4.6767e-02, -1.3679e-02,  3.9562e-03,  1.0087e-04],
         [-3.5474e-04,  4.7144e-03,  8.3967e-04, -1.9705e-02, -9.4592e-03,
          -5.8859e-03,  1.0172e-03,  9.2020e-04, -2.0059e-04],
         [ 2.9056e-03,  1.6125e-04, -4.0626e-04, -8.0189e-03,  1.3228e-03,
          -5.3636e-04, -7.3536e-04,  3.4558e-05,  1.4845e-04],
         [-1.2475e-04, -4.9942e-04, -2.6091e-04, -5.6161e-04,  8.3187e-05,
          -1.2714e-04, -2.1174e-04,  4.1940e-06, -4.5643e-05]],

        [[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  9.9909e-01,
          -6.8512e-02, -8.1567e-02,  2.5140e-02, -2.4035e-03],
         [-3.4328e-03,  1.6768e-02,  1.2305e-02, -3.6708e-02,  1.0285e-01,
           1.1224e-02, -2.3418e-02, -5.4137e-04,  9.3986e-04],
         [-2.8389e-03,  1.4652e-03,  1.0112e-03,  9.8102e-04, -2.3162e-02,
          -6.1180e-03,  1.5327e-03,  9.4122e-04, -1.2781e-03],
         [ 3.9240e-04, -2.3131e-04,  4.5690e-04, -3.8244e-03, -1.5314e-03,
           1.8863e-03,  1.1882e-03, -5.2338e-04,  2.6766e-04],
         [-2.8441e-04, -3.4162e-04,  5.4013e-05,  7.4252e-04,  4.9895e-04,
          -6.1110e-04, -8.7185e-04, -1.1714e-04,  9.9285e-08]],

        [[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  1.0000e+00,
           6.9176e-02, -1.8489e-02, -6.5094e-03, -7.6238e-04],
         [ 1.4062e-03,  4.2645e-03, -1.0647e-02, -8.1579e-02,  1.0522e-01,
           1.6914e-02,  6.5321e-04,  6.9397e-04,  2.0881e-04],
         [-6.5155e-05, -1.2232e-03, -3.3660e-03,  9.8742e-03, -1.4611e-02,
           6.0985e-03,  9.5693e-04, -1.0049e-04,  5.4173e-05],
         [-4.3969e-04, -5.1155e-04,  6.9611e-03, -2.8698e-04, -5.8589e-03,
          -5.4844e-05, -7.3797e-04, -5.4401e-06, -3.3698e-05],
         [-1.9741e-04,  1.0003e-04, -2.0176e-04,  4.9546e-04, -1.6201e-04,
          -1.9169e-04, -3.9886e-04,  3.3773e-05, -3.5972e-05]],

        [[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  1.0000e+00,
           1.1652e-01, -1.5593e-02, -1.0215e-02, -1.8656e-03],
         [ 3.1697e-03,  2.1618e-02,  2.7072e-02, -2.4032e-02,  8.6125e-02,
          -7.1168e-04, -1.2433e-02, -2.0902e-03,  1.5868e-04],
         [-2.3877e-04, -4.9871e-03, -2.4145e-02, -2.1623e-02, -3.1477e-02,
          -8.3460e-03, -8.8675e-04, -5.3290e-04, -2.2784e-04],
         [-1.0006e-03,  2.1055e-05, -1.7186e-03, -5.2886e-03,  4.5186e-03,
          -1.1530e-03,  6.2732e-05,  1.4212e-04,  4.3367e-05],
         [ 7.8993e-05, -3.9503e-04,  1.5458e-03, -4.9707e-04, -3.9470e-04,
           6.0808e-04, -3.6447e-04,  1.2936e-04,  6.3461e-07]]]),
 'boundary.z_sin': tensor([[[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,
          -1.4295e-02,  1.4929e-02, -6.6461e-03, -3.0652e-04],
         [ 9.6958e-05, -1.6067e-03,  5.7568e-02, -2.2848e-02, -1.6101e-01,
           1.6560e-02,  1.5032e-02, -1.2463e-03, -4.0128e-04],
         [-9.9541e-04,  3.6108e-03, -1.1401e-02, -1.8894e-02, -7.7459e-04,
           9.4527e-03, -4.6871e-04, -5.5180e-04,  3.2248e-04],
         [ 2.3465e-03, -2.4885e-03, -8.4212e-03,  8.9649e-03, -1.9880e-03,
          -1.6269e-03,  8.4700e-04,  3.7171e-04, -6.8400e-05],
         [-3.6228e-04, -1.8575e-04,  6.0890e-04,  5.0270e-04, -6.9953e-04,
          -7.6356e-05,  2.3796e-04, -3.2524e-05,  5.3396e-05]],

        [[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,
          -8.5341e-02,  2.4825e-02,  8.0996e-03, -7.1501e-03],
         [-1.3470e-03,  4.6367e-03,  4.1579e-02, -3.6802e-02, -1.5076e-01,
           7.1852e-02, -1.9793e-02,  8.2575e-03, -3.8958e-03],
         [-2.3956e-03, -5.7497e-03,  5.8264e-03,  9.4471e-03, -3.5171e-03,
          -1.0481e-02, -3.2885e-03,  4.0624e-03,  4.3130e-04],
         [ 6.3403e-05, -9.2162e-04, -2.4765e-03,  5.4090e-04,  1.9999e-03,
          -1.1500e-03,  2.7581e-03, -5.7271e-04,  3.0363e-04],
         [ 4.6278e-04,  4.3696e-04,  8.0524e-05, -2.4660e-04, -2.3747e-04,
           5.5060e-05, -1.3221e-04, -5.4823e-05,  1.6025e-04]],

        [[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,
          -1.6090e-01, -1.4364e-02,  3.7923e-03,  1.8234e-03],
         [ 1.2118e-03,  3.1261e-03,  3.2037e-03, -5.7482e-02, -1.5461e-01,
          -1.8058e-03, -5.7149e-03, -7.4521e-04,  2.9463e-04],
         [ 8.7049e-04, -3.2717e-04, -1.0188e-02,  1.1215e-02, -7.4697e-03,
          -1.3592e-03, -1.4984e-03, -3.1362e-04,  1.5780e-06],
         [ 1.2617e-04, -1.2257e-04, -6.9928e-04,  8.7431e-04, -2.5848e-03,
           1.2087e-03, -2.4723e-04, -1.6535e-05, -6.4372e-05],
         [-4.3932e-04, -1.8130e-04,  7.4368e-04, -6.1396e-04, -4.1518e-04,
           4.8132e-04,  1.6036e-04,  5.3081e-05,  1.6636e-05]],

        [[ 0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,  0.0000e+00,
          -1.1264e-02, -1.8349e-03,  7.2464e-03,  2.3807e-03],
         [ 3.2969e-03,  1.9590e-02,  2.8355e-02, -1.0493e-02, -1.3216e-01,
           1.7804e-02,  7.9768e-03,  2.1362e-03, -6.9118e-04],
         [-5.2572e-04, -4.1409e-03, -3.6560e-02,  2.1644e-02,  1.6418e-02,
           9.3557e-03,  3.3846e-03,  7.4172e-05,  1.8406e-04],
         [-1.4907e-03,  2.0496e-03, -4.8581e-03,  3.5471e-03, -2.9191e-03,
          -1.5056e-03,  7.7168e-04, -2.3136e-04, -1.2064e-05],
         [-2.3742e-04,  4.5083e-04, -1.2933e-03, -4.4028e-04,  6.4168e-04,
          -8.2755e-04,  4.1233e-04, -1.1037e-04, -6.3762e-06]]]),
 'metrics.aspect_ratio': tensor([9.6474, 9.1036, 9.4119, 9.5872]),
 'metrics.aspect_ratio_over_edge_rotational_transform': tensor([  9.3211, 106.7966,  13.8752,   8.9834]),
 'metrics.average_triangularity': tensor([-0.6456, -0.5325, -0.6086, -0.6531]),
 'metrics.axis_magnetic_mirror_ratio': tensor([0.2823, 0.4224, 0.2821, 0.2213]),
 'metrics.axis_rotational_transform_over_n_field_periods': tensor([0.2333, 0.0818, 0.1887, 0.1509]),
 'metrics.edge_magnetic_mirror_ratio': tensor([0.4869, 0.5507, 0.3029, 0.2991]),
 'metrics.edge_rotational_transform_over_n_field_periods': tensor([0.3450, 0.0284, 0.2261, 0.3557]),
 'metrics.flux_compression_in_regions_of_bad_curvature': tensor([1.4084, 0.9789, 1.5391, 1.1138]),
 'metrics.max_elongation': tensor([6.7565, 6.9036, 5.6105, 5.8703]),
 'metrics.minimum_normalized_magnetic_gradient_scale_length': tensor([5.9777, 4.2971, 8.5928, 4.8531]),
 'metrics.qi': tensor([0.0148, 0.0157, 0.0016, 0.0248]),
 'metrics.vacuum_well': tensor([-0.2297, -0.1146, -0.0983, -0.1738])}
```
</details>
</div>

### Advanced Usage
For advanced manipulation and visualization of data contained in this dataset, install `constellaration` from [here](https://github.com/proximafusion/constellaration):
`pip install constellaration`

Load and instantiate plasma boundaries:
```python
from constellaration.geometry import surface_rz_fourier

ds = datasets.load_dataset(
    "proxima-fusion/constellaration",
    columns=["plasma_config_id", "boundary.json"],
    split="train",
    num_proc=4,
)
pandas_ds = ds.to_pandas().set_index("plasma_config_id")

plasma_config_id = "DQ4abEQAQjFPGp9nPQN9Vjf"
boundary_json = pandas_ds.loc[plasma_config_id]["boundary.json"]
boundary = surface_rz_fourier.SurfaceRZFourier.model_validate_json(boundary_json)
```
Plot boundary:
```python
from constellaration.utils import visualization

visualization.plot_surface(boundary).show()
visualization.plot_boundary(boundary).get_figure().show()
```
Boundary                   | Cross-sections
:-------------------------:|:-------------------------:
![Plot of plasma boundary](assets/boundary.png) | ![Plot of boundary cross-sections](assets/boundary_cross_sections.png)

Stream and instantiate the VMEC ideal MHD equilibria:
```python
from constellaration.mhd import vmec_utils

wout_ds = datasets.load_dataset(
    "proxima-fusion/constellaration",
    "vmecpp_wout",
    split="train",
    streaming=True,
)

row = next(wout_ds.__iter__())

vmecpp_wout_json = row["json"]
vmecpp_wout = vmec_utils.VmecppWOut.model_validate_json(vmecpp_wout_json)

# Fetch corresponding boundary

plasma_config_id = row["plasma_config_id"]
boundary_json = pandas_ds.loc[plasma_config_id]["boundary.json"]
boundary = surface_rz_fourier.SurfaceRZFourier.model_validate_json(boundary_json)
```
Plot flux surfaces:
```python
from constellaration.utils import visualization

visualization.plot_flux_surfaces(vmecpp_wout, boundary)
```
![Plot of flux surfaces](assets/flux_surfaces.png)

Save ideal MHD equilibrium to *VMEC2000 WOut* file:
```python
import pathlib
from constellaration.utils import file_exporter

file_exporter.to_vmec2000_wout_file(vmecpp_wout, pathlib.Path("vmec2000_wout.nc"))
```
Match the boundaries from the **default** dataset to the corresponding metrics under a certain plasma condition:
```python
import datasets

# Load default dataset to get the boundaries
default_ds = datasets.load_dataset(
    "proxima-fusion/constellaration",
    split="train",
    num_proc=4,
)

# Load finite beta 3% dataset
finite_beta_3pct_ds = datasets.load_dataset(
    "proxima-fusion/constellaration",
    name="finite_beta_3pct",
    split="train",
    num_proc=4,
)

# Join the two datasets on plasma_config_id <-> misc.source_plasma_config_id
default_df = (
    default_ds
    .to_pandas()
    .set_index("plasma_config_id")
    .filter(like="boundary.")
)
finite_beta_3pct_df = (
    finite_beta_3pct_ds
    .to_pandas()
    .set_index("misc.source_plasma_config_id")
)
finite_beta_3pct_with_boundaries_df = (
    finite_beta_3pct_df
    .join(default_df, how="inner")  # joins on index
    .reset_index(names="misc.source_plasma_config_id")
)
```

## Dataset Creation

### Curation Rationale

<!-- Motivation for the creation of this dataset. -->

Wide-spread community progress is currently bottlenecked by the lack of standardized optimization problems with strong baselines and datasets that enable data-driven approaches, particularly for quasi-isodynamic (QI) stellarator configurations.

### Source Data

<!-- This section describes the source data (e.g. news text and headlines, social media posts, translated sentences, ...). -->

#### Data Collection and Processing

<!-- This section describes the data collection and processing process such as data selection criteria, filtering and normalization methods, tools and libraries used, etc. -->

We generated this dataset by sampling diverse QI fields and optimizing stellarator plasma boundaries to target key properties, using four different methods.

#### Who are the source data producers?

<!-- This section describes the people or systems who originally created the data. It should also include self-reported demographic or identity information for the source data creators if this information is available. -->

Proxima Fusion's stellarator optimization team.

#### Personal and Sensitive Information

<!-- State whether the dataset contains data that might be considered personal, sensitive, or private (e.g., data that reveals addresses, uniquely identifiable names or aliases, racial or ethnic origins, sexual orientations, religious beliefs, political opinions, financial or health data, etc.). If efforts were made to anonymize the data, describe the anonymization process. -->

The dataset contains no personally identifiable information.

## Citation

<!-- If there is a paper or blog post introducing the dataset, the APA and Bibtex information for that should go in this section. -->

**BibTeX:**

```
@article{cadena2025constellaration,
  title={ConStellaration: A dataset of QI-like stellarator plasma boundaries and optimization benchmarks},
  author={Cadena, Santiago A and Merlo, Andrea and Laude, Emanuel and Bauer, Alexander and Agrawal, Atul and Pascu, Maria and Savtchouk, Marija and Guiraud, Enrico and Bonauer, Lukas and Hudson, Stuart and others},
  journal={arXiv preprint arXiv:2506.19583},
  year={2025}
}
```

## Glossary

<!-- If relevant, include terms and calculations in this section that can help readers understand the dataset or dataset card. -->

| Abbreviation | Expansion |
| -------- | ------- |
| QI | Quasi-Isodynamic(ity) |
| MHD | Magneto-Hydrodynamic |
| [DESC](https://desc-docs.readthedocs.io/en/stable/) | Dynamical Equilibrium Solver for Confinement |
| VMEC/[VMEC++](https://github.com/proximafusion/vmecpp) | Variational Moments Equilibrium Code (Fortran/C++) |
| QP | Quasi-Poloidal |
| NAE | Near-Axis Expansion |
| NFP | Number of Field Periods |

## Dataset Card Authors

Alexander Bauer, Santiago A. Cadena

## Dataset Card Contact

scadena@proximafusion.com