# Overview

Fog is notoriously difficult to predict.  Numerical models struggle with the complex near-surface processes and microphysics.
Most methods rely on a quasi-nowcasting semi-heuristic approach based on current observed temperature and humidity.

The occurrence of fog at a particular aerodrome has a strong seasonal climatological signal. Processes behind this signal, in order of significance, are length of night, cooling rates, ground (surface and sub-surface) temperature and moisture, sea (and other nearby water bodies) surface temperature, and climatological weather patterns affecting wind, moisture transport etc.  Further, different fog processes may dominate at different locations and at different times of year, the dominant ones being radiation and advection fogs.

On a finer temporal scale, fog occurrence relies on the cooling, distribution and finally condensation and maintenance of the pre-existing moisture.  This in turn requires radiational loss through minimal cloud thickness, with radiational loss further assisted by low mid-level humidity.  Low surface wind is also critical to allow a surface inversion layer to form, while non-zero wind can assist in preventing forming droplets from depositing to ground (while redistributing condensed dew moisture  into the air).  Frost on the other hand can be an effective remover of humidity.  Finally, the nuclei species can tip the balance.  Even high resolution models struggle with, or have no knowledge of,  these processes.

Instead of relying on a model to predict fog, this proposal uses the more reliable signals from NWP to refine the climatological occurrence of fog, and in turn use those reliable model signals for future prediction.  ‘Reliable signals’ are a function of parameter and lead-time, but with a focus on 36 (24?)-72 (120?) hour prediction, surface pressure distribution at the synoptic scale (~1000km) has good predictability and is likely to have strong correlation to fog occurrence.  Correlating seasonal fog occurrence with these reliable model signals should enable us to refine the climatological expectation of fog to a useful prediction. Even relatively low levels of ‘skill’ may be valuable.

Suggest focussing on NZCH (Christchurch) initially as fog is relatively common, fog occurrence has high impact, mod-poor predictability and should show reasonable synoptic and seasonal correlations.  NZHN (Hamilton) would be a good second test case as fog is frequent and easier to forecast, while NZAA (Auckland) would provide a good test of skill, having highest impact with relatively few events, poor predictability, and likely reasonable but more complex synoptic correlations.

# Market/need

Meteorological phenomena are the most costly and disruptive factors in aircraft operations (outside less predictable factors such as fuel costs, market forces or regulation, about which little can be done).  Of these, aerodrome fog and convection/thunderstorms are the most significant, costing airlines and industrial operations that rely on aircraft a significant part of their balance sheet.  Current methods of fog prediction have low skill and have short lead-times: a 30% fog prediction for ‘tonight’ (i.e. a 12-18 hour prediction) is considered a valuable forecast while predictions seldom go above 50%.  Yet these typically have poor success measures: PoD (prob of detection) is often near 50% and FAR (false alarm rates) can be well over 100%.

The method proposed here is not focussed on the short-term, where nowcast methods will likely still be superior, although some comparison could be interesting, and the method may yet provide a useful objective tool at that range.  Instead, the method will have the greatest utility at the next-day (~36 hour forecast) level and beyond for which no method presently dominates.  Further, the method should retain skill at the level of the underlying NWP, which at the scales suggested, should be through 72, even 120, hours.  This would improve airline planning.

Further, a probabilistic forecast that is well calibrated and reliable would have significant utility and market advantage.  Probabilistic forecasts exist, however they are set at 30, 40, 50% likelihood and are based on forecaster judgement alone and have little skill.  Reliable probabilities could revolutionise aviation planning, which will necessarily become more refined in terms of probabilistic risk measures in future.

# Method

1. Identify fog ‘events’ in an aerodrome observation record (3-20 years, depending on the frequency of fog at that site).  This is likely best through visibility measurements and possibly with secondary checks on humidity (and possibly precipitation, to discriminate).  Defining an event is important – I would suggest a 2-hour period of significant visibility reduction as this is an operationally-significant event and removes ‘noise’ from transitory brief conditions.  Also, I would suggest not including time: the signal we wish to identify is the occurrence of fog on a particular night period (perhaps based on the astronomical hours of darkness for that location).  Pinning down timing is a different prediction problem (more suited to a short time horizon), and has different implications for users - the greater market need is knowledge about the likelihood of fog causing disruption on a particular night.

    - A possible exception to the above are ‘sunrise fogs’ that only occur with the mixing provided by sunrise.  This may include fogs that persist through the morning well after sunrise.  An option could be to treat these separately.  I would expect them to have very similar predictive characteristics to the overnight fogs, but could be worth confirming this.

    - Another possible exception are advective fogs which have different formation characteristics from the more typical radiation fogs.  As a result, these will likely have different time-of-day and climatological signals.  However, they are mostly seen at NZWN and are considered rare at any of NZCH, NZAA, NZHN.  NZWN could be investigated separately if skill is first shown at the other locations.

    - We have previously applied ‘fog occurrence’ identification algorithms to aerodrome observations. These are robust and can be reused.

2. Once a set of observed ‘fog nights’ is obtained, identify signals in the NWP that are associated with them.  By applying classification or clustering, or other categorisations to the NWP,  it is expected that the majority of fogs will share common characteristics in terms of broad flow regime and/or airmass.  An optimal number of classes (perhaps 3-6) should be identified that span the observed events while providing discrimination between them.  There may be rare or unusual events that result in outlier categories with few members.

    - Recommended inputs/fields for the analysis  could be:

        * MSLP across a broad domain to represent overall synoptic regime and likely local flow (the smaller the domain and higher the resolution, the more likely local flow will be represented, however this may also introduce more noise).

        * 925hPa Theta-w locally to represent boundary layer moisture.  Could consider other levels, or Td, q (specific humidity), however likely wish to avoid surface parameters due to low predictability/noise.  A  point over the station may be sufficient, though could investigate using other representative locations (or averages or even fields).

        * A local wind (e.g. 850 hPa at the station)  could be considered, though this should be sufficiently captured by the MSLP.

        * Suggest using a set prognosis period in the first instance, e.g. short range, such as the earlier prior run (so midday of the day before the night in question).  We are then assessing NWP ‘skill’ or correlations in the short range, but later can extend to the next day observed events, and then the next, re-calibrating the climatological occurrence for that time period each time.

        * Could consider use of observations in this set (e.g. previously observed dewpoint, ground temperatures…), however I’d not want to do this in the first instance

3. Once categories or classes of NWP have been obtained for the fog events, a method needs to be developed to invert the association, such that NWP signals can be identified as belonging to a fog occurrence class or not.  A simple method may be using least squares against a reference NWP field for each class.  The tolerance setting for identifying whether the test confirms the prognosed NWP belongs to a fog class or not is a crucial parameter: it may be estimated by the variance within the fog classes themselves, or later tweaked to optimise the POD/FAR of the overall method.

4. With sets of NWP representing the various fog occurrence classes, and a test for identifying whether a particular NWP run falls within one of the sets or not, the climatological calibration (or relative occurrences) can be determined.   This would naturally be done at a daily resolution, that is, calibrations done for each day, but coarser calibrations could be considered.  To increase the number of fog events sampled and lessen noise, a time window can be used to include a certain number of days either side.  The number of fog events observed within that window, divided by the number of times NWP matched a fog occurrence classification,gives the relative frequency of fog for that classification for that ‘day’.

    - Suggest a window of 15 days either side for each day’s calibration for NZCH (possibly less for NZHN, but a longer period may be required for NZAA).  Longer periods will start to lose the seasonal or other climate signals; shorter periods will lessen the events and increase noise.  This number can later be optimised for predictive results.

    - The above is relatively straightforward for a ‘next day forecast’ (using NWP from the previous run for each night’s prediction).  Calibrations would need to be re-done using the same run for each subsequent day to yield a climatological occurrence that accounted for model drift at subsequent day’s lead-time.  The amount of repetition here provides opportunity for efficient repurposing of the analysis.

# Data

Observational data is readily available: most national weather services offer free historic data downloads and these cover most aerodromes.  In NZ this is via CliFlo run by NIWA.  Temp (T) and Humidity (Td, RH, Tw) are available hourly, as well as visibility (in m, via calibrated IR extinction coefficient) for most aerodromes.  These records go back at least 10 years for major aerodromes.

Model data can be downloaded for free (confirm – some limitation for non accredited users, but suspect not an issue) from the ECMWF MARS interface (though clunky!).  Could consider reanalysis data, but operational data is more appropriate for calibration when being applied to forecast NWP.  Difficult to allow for model upgrades over the period, though these are likely to be minimal in most respects depending on lead-times and resolution of features.
# Challenges / Opportunities for improved approaches

Comparative performance metrics for the method would be pure climatology and pure NWP (via visibility).
