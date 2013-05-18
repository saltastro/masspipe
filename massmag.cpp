/** MASS color equation coefficient from linear regression of a synthetic                                                     
    relation Mag_{mass}-V vs (B-V)_0:  Mag_{mass} = V + MASSCE * (B-V) */
//const double MASSCE = 0.5905; //for original MASS                                                                           
//const double MASSCE = 0.347; //for MASS-DIMM (with cut-off filter)                                                          
const double MASSCE = 0.56;
/**                                                                                                                           
        @brief  Convert the Johnson V-magnitude into MASS magnitude                                                           
        @param  vmag    V-band magnitude                                                                                      
        @param  bv              B-V color                                                                                     
        @param  coleq   Linear color equation coefficient                                                                     
                                                                                                                              
        This function converts the standard V-magnitude of a star into the                                                    
        MASS-band magnitude using the linear color equation with a coefficient \a                                             
        coleq. By default, this coefficient is taken from the module constant                                                 
        sum::MASSCE. For a star having (B-V)==0 (A0), the MASS magnitude is assumed to                                        
        be equal to V-magnitude.                                                                                              
                                                                                                                              
*/
inline double massmag(double vmag, double bv, double coleq = sum::MASSCE)
{
  return vmag + bv * coleq ;
}
