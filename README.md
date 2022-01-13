# Overview

Fog is notoriously difficult to predict.  Numerical models struggle with the complex near-surface processes and microphysics.
Most methods rely on a quasi-nowcasting semi-heuristic approach based on current observed temperature and humidity.
The occurrence of fog at a particular aerodrome has a strong seasonal climatological signal.

Processes behind this signal, in order of significance, are length of night, cooling rates, ground (surface and sub-surface) temperature and moisture, sea (and other nearby water bodies) surface temperature, and climatological weather patterns affecting wind, moisture transport etc.  Further, different fog processes may dominate at different locations and at different times of year, the dominant ones being radiation and advection fogs.

On a finer temporal scale, fog occurrence relies on the cooling, distribution and finally condensation and maintenance of the pre-existing moisture.  This in turn requires radiational loss through minimal cloud thickness, with radiational loss further assisted by low mid-level humidity.  Low surface wind is also critical to allow a surface inversion layer to form, while non-zero wind can assist in preventing forming droplets from depositing to ground (while redistributing condensed dew moisture  into the air).  Frost on the other hand can be an effective remover of humidity.  Finally, the nuclei species can tip the balance.  Even high resolution models struggle with, or have no knowledge of,  these processes.

Instead of relying on a model to predict fog, this proposal uses the more reliable signals from NWP to refine the climatological occurrence of fog, and in turn use those reliable model signals for future prediction.  ‘Reliable signals’ are a function of parameter and lead-time, but with a focus on 36 (24?)-72 (120?) hour prediction, surface pressure distribution at the synoptic scale (~1000km) has good predictability and is likely to have strong correlation to fog occurrence.  Correlating seasonal fog occurrence with these reliable model signals should enable us to refine the climatological expectation of fog to a useful prediction. Even relatively low levels of ‘skill’ may be valuable.

Focussing on NZCH (Christchurch) initially as fog is relatively common, fog occurrence has high impact, mod-poor predictability and should show reasonable synoptic and seasonal correlations.  NZHN (Hamilton) would be a good second test case as fog is frequent and easier to forecast, while NZAA (Auckland) would provide a good test of skill, having highest impact with relatively few events, poor predictability, and likely reasonable but more complex synoptic correlations.

# Market/need

Meteorological phenomena are the most costly and disruptive factors in aircraft operations (outside less predictable factors such as fuel costs, market forces or regulation, about which little can be done).  Of these, aerodrome fog and convection/thunderstorms are the most significant, costing airlines and industrial operations that rely on aircraft a significant part of their balance sheet.  Current methods of fog prediction have low skill and have short lead-times: a 30% fog prediction for ‘tonight’ (i.e. a 12-18 hour prediction) is considered a valuable forecast while predictions seldom go above 50%.  Yet these typically have poor success measures: PoD (prob of detection) is often near 50% and FAR (false alarm rates) can be well over 100%.

The method proposed here is not focussed on the short-term, where nowcast methods will likely still be superior, although some comparison could be interesting, and the method may yet provide a useful objective tool at that range.  Instead, the method will have the greatesthave greatest utility at the next-day (~36 hour forecast) level and beyond for which no method presently dominates.  Further, the method should retain skill at the level of the underlyingunderlyng NWP, which at the scales suggested, should be through 72, even 120, hours.  This would improve airline planning.

Further, a probabilistic forecast that is well calibrated and reliable would have significant utility and market advantage.  Probabilistic forecasts exist, however they are set at 30, 40, 50% likelihood and are based on forecaster judgement alone and have little skill.  Reliable probabilities could revolutionise aviation planning, which will necessarily become more refined in terms of probabilistic risk measures in future.

# Method

- Identify fog ‘events’ in an aerodrome observation record (3-20 years, depending on the frequency of fog at that site).  This is likely best through visibility measurements and possibly with secondary checks on humidity.  Defining an event is important – I would suggest a 2-hour period of significant visibility reduction as this is an operationally-significant event and removes ‘noise’ from transitory brief conditions.  Also, I would suggest not including time – the signal to identify is the occurrence of fog on a particular night period (perhaps based on the astronomical hours of darkness for that location) not to pin down the timing.

- One possible exception to the above are ‘sunrise fogs’ that only occur with the mixing provided by sunrise.  This may include fogs that persist through the morning well after sunrise.  An option could be to treat these separately, or simply include in the analysis of night-time fogs.

# Data

Observational data is readily available: most national weather services offer free historic data downloads and these cover most aerodromes.  In NZ this is via CliFlo run by NIWA.  Temp (T) and Humidity (Td, RH, Tw) are available hourly, as well as visibility (in m, via calibrated IR extinction coefficient) for most aerodromes.  These records go back at least 10 years for major aerodromes.

Model data can be downloaded for free (confirm – some limitation for non accredited users, but suspect not an issue) from the ECMWF MARS interface (though clunky!).  Could consider reanalysis data, but operational data is more appropriate for calibration when being applied to forecast NWP.  Difficult to allow for model upgrades over the period, though these are likely to be minimal in most respects depending on lead-times and resolution of features.

# Challenges / Opportunities for improved approaches

Comparative performance metrics for the method would be pure climatology and pure NWP (via visibility).
