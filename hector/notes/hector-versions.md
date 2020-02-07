# Overview of Hector Release Versions


| Version | Release Date | Commit   | Remarks  |
| :-----: | :----------: | :------: | :------ |
| 2.3.0   | 2 Jan 2020   | [`16c480a`](https://github.com/JGCRI/hector/commit/16c480ae951000adda287d84c02b3d58f538d48c) | Constrain atmospheric CO2 concentration during the model spinup |
| 2.2.2   | 4 May 2019   | [`fddfed5`](https://github.com/JGCRI/hector/commit/fddfed55c262edf1eb068a4ef63e48bc35d05ff8) | Introduce R Hector interface |
| 2.2.0   | 25 Mar 2019  | [`6a8f89b`](https://github.com/JGCRI/hector/commit/6a8f89b48d5427548929634d4d2fe0dea28c8217) | Add `VOLCANIC_SCALE` parameter |
| 2.0.1   | 19 Mar 2019  | [`b52ded1`](https://github.com/JGCRI/hector/commit/b52ded1ec7c74f95729ef8e1064badb9a63b121f) | Incorporated DOECLIM ocean heat model |
| 1.1.4   | 30 Jun 2017  | [`ec9af49`](https://github.com/JGCRI/hector/commit/ec9af49fccc34fc857c2745f3ea3d691b48984d7) | GSL libraries no longer required |
| 1.1.3   | 23 Feb 2016  | [`7f87172`](https://github.com/JGCRI/hector/commit/7f87172a75112c48ae0b29f84194ee593c26f709) | Model returns nonzero exit code on error|
| 1.1.2   | 19 Nov 2015  | [`b66a15d`](https://github.com/JGCRI/hector/commit/b66a15d5e0a39b9fdc905b8910c228caef9977d9) | Add libhector build target for MacOS & Win |
| 1.1.1   | 26 Aug 2015  | [`cf4d643`](https://github.com/JGCRI/hector/commit/cf4d6435d4ad21bf38c00ff81ef4556dc51ebe03) | Update sample output files |
| 1.1.0   | 24 Aug 2015  | [`12db882`](https://github.com/JGCRI/hector/commit/12db8826e196d7883b0f4c5f6b36de290f422ce8) | API for linking with external models |
| 1.0.0   | 31 Mar 2015  | [`987d1ac`](https://github.com/JGCRI/hector/commit/987d1acfac8043d572d9ed5dd1504b129be83906) | Published in Hartin et al. GMD paper |
| 0.1.0   | 29 Sep 2014  | [`39e734e`](https://github.com/JGCRI/hector/commit/39e734e3abab8dc808f0447bb1793454788500c7) | Submitted to GMDD |

<br>

## Version 2.3.0
**Released**: 2 Jan 2020 <br>
**Commit**: [`16c480a`](https://github.com/JGCRI/hector/commit/16c480ae951000adda287d84c02b3d58f538d48c)

* Constrain atmospheric CO2 concentration to be equal to the preindustrial concentration during the model spinup. The result of this is that the concentration at the beginning of the simulation will be equal to the value specified in the `PREINDUSTRIAL_CO2` parameter, which was not the case in previous versions.
  
  
## Version 2.2.2
**Released**: 4 May 2019 <br>
**Commit**: [`fddfed5`](https://github.com/JGCRI/hector/commit/fddfed55c262edf1eb068a4ef63e48bc35d05ff8)

* **First appearance of R Hector interface**
* Fix bug that was causing requests for H2O forcing in the R interface to return N2O forcing instead (the model internals were unaffected).
* Fix bug that was causing API requests for halocarbon forcing to return absolute forcing values, rather than values relative to the base year (which is what is done for all other forcings).
* Add missing capability dependency in forcing component.


## Version 2.2.0
**Released**: 25 Mar 2019
**Commit**: [`6a8f89b`](https://github.com/JGCRI/hector/commit/6a8f89b48d5427548929634d4d2fe0dea28c8217)

* Add a new parameter: VOLCANIC_SCALE. This parameter adjusts the strength of the response to volcanic forcing. (PR [#291](https://github.com/JGCRI/hector/pull/291))
* Add getname function to return the name of a Hector core.


## Version 2.0.1
**Released**: 19 Mar 2019
**Commit**: [`b52ded1`](https://github.com/JGCRI/hector/commit/b52ded1ec7c74f95729ef8e1064badb9a63b121f)

* Updated license - intended to be GPLv3
* Incorporated 1-D diffusive ocean heat model as new temperature component (DOECLIM) (PR [#206](https://github.com/JGCRI/hector/pull/206))
* Bugfix: double counting halocarbon radiative forcing (PR [#201](https://github.com/JGCRI/hector/pull/201))
* Bugfix: re-enabled CO2 concentration constraint (PR [#163](https://github.com/JGCRI/hector/pull/163))
* Various changes to internals to support calling Hector from external code like pyhector
* Component loggers are now optional (PR [#218](https://github.com/JGCRI/hector/pull/218))
* Renamed anthro emissions to ffi emisisons (fossil fuel industrial) (PR [#116](https://github.com/JGCRI/hector/pull/116))
* `Hector-2.0.1-Windows.zip` with a Windows executable file
* `Hector-2.0.1-MacOSx.zip` with a MacOS executable file


## Version 1.1.4
**Released**: 30 Jun 2017
**Commit**: [`ec9af49`](https://github.com/JGCRI/hector/commit/ec9af49fccc34fc857c2745f3ea3d691b48984d7)

* Fix bug in CO2 constraint capability.
* GSL libraries no longer required.


## Version 1.1.3
**Released**: 23 Feb 2016 
**Commit**: [`7f87172`](https://github.com/JGCRI/hector/commit/7f87172a75112c48ae0b29f84194ee593c26f709)

* Model now returns nonzero exit code on error
* Compiles correctly on newer Visual Studio


## Version 1.1.2
**Released**: 19 Nov 2015
**Commit**: [`b66a15d`](https://github.com/JGCRI/hector/commit/b66a15d5e0a39b9fdc905b8910c228caef9977d9)

* Adds the libhector build target to the OS X and Windows project files (it was already available in the Linux build). This library is needed in order to link Hector to an outside model
* There are no changes to the model behavior relative to v.1.1.1.


## Version 1.1.1
**Released**: 26 Aug 2015
**Commit**: [`cf4d643`](https://github.com/JGCRI/hector/commit/cf4d6435d4ad21bf38c00ff81ef4556dc51ebe03)

* Fix OS X build.
* Update sample output files
* Add GPL license


## Version 1.1.0
**Released**: 24 Aug 2015
**Commit**: [`12db882`](https://github.com/JGCRI/hector/commit/12db8826e196d7883b0f4c5f6b36de290f422ce8)

* API for linking with external models.
* Backend R scripts faster and cleaner.
* Minor bug fixes and documentation updates.


## Version 1.0.0
**Released**: 31 Mar 2015
**Commit**: [`987d1ac`](https://github.com/JGCRI/hector/commit/987d1acfac8043d572d9ed5dd1504b129be83906)

* Hector version 1.0, including all code and outputs supporting the published Hartin et al. GMD paper.


## Version 0.1.0
**Released**: 29 Sep 2014
**Commit**: [`39e734e`](https://github.com/JGCRI/hector/commit/39e734e3abab8dc808f0447bb1793454788500c7)

* Submitted to GMDD.
