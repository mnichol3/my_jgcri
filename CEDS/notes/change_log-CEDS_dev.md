# CEDS-dev Change Log
Change log for CEDS-dev fork intalled on the pic HPC cluster.

* **2020-04-28** (Tues)
  * `rlang` version downgraded from `0.4.4` to `0.3.1`.
    * Associated `renv::snapshot()` warnings:
      * `'tidyselect' requires 'rlang (>= 0.4.3)'`
      * `'vctrs     ' requires 'rlang (>= 0.4.2)'`
      * `'lifecycle ' requires 'rlang (>= 0.4.0)'`
    * Side-effects
      * `XML       [3.99-0.3 -> *]`
      * `reshape   [0.8.6 -> *]`
